import os, json, re
import numpy as np
from pathlib import Path
from rank_bm25 import BM25Okapi
import faiss
from llm import LLM


INDEX_DIR = Path(".index")
FAISS_FILE = INDEX_DIR / "faiss.index"
META_FILE = INDEX_DIR / "meta.json"
BM25_FILE = INDEX_DIR / "bm25.json"


class HybridRetriever:
def __init__(self):
self.meta = json.loads(Path(META_FILE).read_text(encoding="utf-8"))
self.index = faiss.read_index(str(FAISS_FILE))
bm = json.loads(Path(BM25_FILE).read_text(encoding="utf-8"))
self.bm25 = BM25Okapi(bm["corpus"]) if bm else None
self.texts = [m["text"] for m in self.meta]


async def search(self, query: str, k: int = 4, alpha: float = 0.5):
# dense
llm = LLM()
qv = (await llm.embed([query]))[0]
qv = np.array([qv], dtype="float32")
faiss.normalize_L2(qv)
sims, idx = self.index.search(qv, k)
dense_scores = sims[0].tolist()
dense_ids = idx[0].tolist()


# sparse
toks = [t.lower() for t in re.findall(r"\w+", query)]
sparse_scores = self.bm25.get_scores(toks).tolist() if self.bm25 else [0.0]*len(self.texts)


# combine (linear)
combined = []
for rank, (di, dscore) in enumerate(zip(dense_ids, dense_scores)):
sscore = sparse_scores[di]
score = alpha*dscore + (1-alpha)*(sscore/max(1.0, max(sparse_scores)))
combined.append((score, di))
combined.sort(reverse=True)
results = []
for score, di in combined[:k]:
e = self.meta[di]
results.append({"id": e["id"], "text": e["text"], "score": float(score)})
return results
