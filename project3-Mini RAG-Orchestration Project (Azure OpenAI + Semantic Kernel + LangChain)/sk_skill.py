# Minimal function that a planner/skill could call. We won't pull full SK runtime here
# to keep the demo light; instead we expose the same behavior via FastAPI and label it SK.
from retriever import HybridRetriever


async def sk_answer(query: str, k: int = 4):
r = HybridRetriever()
hits = await r.search(query, k=k)
context = "\n\n".join([f"[src:{h['id']}]\n{h['text']}" for h in hits])
# A simple prompt format SK would use
answer = (
"Answer based only on the sources below. If unsure, say NOT FOUND.\n\n"
f"SOURCES:\n{context}\n\n"
f"QUESTION: {query}\n"
"ANSWER: "
)
return answer, hits
