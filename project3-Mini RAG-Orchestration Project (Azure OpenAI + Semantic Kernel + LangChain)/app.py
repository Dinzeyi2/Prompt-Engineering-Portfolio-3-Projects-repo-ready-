import os
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from retriever import HybridRetriever
from sk_skill import sk_answer
from lc_chain import lc_compose


API_KEY = os.getenv("API_KEY")
app = FastAPI(title="Mini RAG Orchestration — SK & LangChain")


class Ask(BaseModel):
question: str
k: int = 4


@app.get("/health")
async def health():
return {"ok": True}


@app.post("/sk/ask")
async def ask_sk(body: Ask, x_api_key: str | None = Header(default=None)):
if API_KEY and x_api_key != API_KEY:
raise HTTPException(status_code=401, detail="Unauthorized")
prompt, hits = await sk_answer(body.question, k=body.k)
# In a full SK app, planner would feed `prompt` to LLM; we do it inline via LangChain-like call
from lc_chain import lc_compose
context = "\n\n".join([f"[src:{h['id']}]\n{h['text']}" for h in hits])
answer = await lc_compose(context, body.question)
return {"answer": answer, "sources": hits}


@app.post("/lc/ask")
async def ask_lc(body: Ask, x_api_key: str | None = Header(default=None)):
if API_KEY and x_api_key != API_KEY:
raise HTTPException(status_code=401, detail="Unauthorized")
r = HybridRetriever()
hits = await r.search(body.question, k=body.k)
context = "\n\n".join([f"[src:{h['id']}]\n{h['text']}" for h in hits])
answer = await lc_compose(context, body.question)
return {"answer": answer, "sources": hits}
