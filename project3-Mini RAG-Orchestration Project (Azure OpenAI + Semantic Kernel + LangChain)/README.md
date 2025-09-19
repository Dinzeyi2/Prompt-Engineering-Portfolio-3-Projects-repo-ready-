# Mini RAG-Orchestration (Azure OpenAI + Semantic Kernel style + LangChain)


This small project demonstrates the orchestration skills Microsoft AI cares about:
- Azure OpenAI integration (with stub fallback)
- Retrieval design (chunking + FAISS dense + BM25 sparse = hybrid)
- Two orchestration styles: SK-ish function and a minimal LangChain chain
- Evidence-required answers with citations


## Quickstart
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.sample .env # fill Azure keys if you have them
python ingest.py # builds .index from data/sample_docs.md
uvicorn app:app --reload --port 8000
