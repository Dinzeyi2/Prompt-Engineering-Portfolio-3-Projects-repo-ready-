import os, re, json
import numpy as np
from pathlib import Path
from rank_bm25 import BM25Okapi
import faiss
from llm import LLM


INDEX_DIR = Path(".index"); INDEX_DIR.mkdir(exist_ok=True)
FAISS_FILE = INDEX_DIR / "faiss.index"
META_FILE = INDEX_DIR / "meta.json"
BM25_FILE = INDEX_DIR / "bm25.json"


CHUNK_SIZE = 500
CHUNK_OVERLAP = 50




def chunk_text(text: str, size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP):
chunks = []
i = 0
while i < len(text):
chunk = text[i:i+size]
chunks.append(chunk)
i += size - overlap
return chunks


async def build():
llm = LLM()
raw = Path("data/sample_docs.md").read_text(encoding="utf-8")
docs = [d.strip() for d in re.split(r"\n\s*# ", raw) if d.strip()]
# Re-add removed hash to section titles for clarity
docs = [("# " + docs[0])] + [("# " + d) for d in docs[1:]] if docs else []


# chunk
entries = []
for did, doc in enumerate(docs):
for cid, ch in enumerate(chunk_text(doc)):
entries.append({"id": f"d{did}_c{cid}", "text": ch, "meta": {"doc": did, "chunk": cid}})


texts = [e["text"] for e in entries]


# embeddings
vecs = await llm.embed(texts)
dim = len(vecs[0])
xb = np.array(vecs, dtype="float32")
index = faiss.IndexFlatIP(dim)
# Normalize for inner product as cosine proxy
faiss.normalize_L2(xb)
index.add(xb)
faiss.write_index(index, str(FAISS_FILE))


# BM25
tokenized = [[t.lower() for t in re.findall(r"\w+", x)] for x in texts]
bm25 = BM25Okapi(tokenized)
Path(BM25_FILE).write_text(json.dumps({"corpus": tokenized}), encoding="utf-8")


# meta
Path(META_FILE).write_text(json.dumps(entries), encoding="utf-8")
print("Indexed:", len(entries), "chunks; dim=", dim)


if __name__ == "__main__":
import asyncio
asyncio.run(build())
