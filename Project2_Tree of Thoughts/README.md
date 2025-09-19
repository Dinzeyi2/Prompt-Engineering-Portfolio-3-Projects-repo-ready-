# Tree of Thoughts (ToT) — FastAPI + Azure‑ready


Production‑ready ToT service implementing BFS & Beam search with pluggable scorers.


## Quickstart
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.sample .env # then fill values (optional)
uvicorn tot.app:app --reload --port 8000
