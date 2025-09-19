from typing import Dict
from pydantic import BaseModel


class SolveRequest(BaseModel):
problem: str
depth: int = 3
thoughts_per_step: int = 3
strategy: str = "beam" # "beam" or "bfs"
beam_width: int = 3
scorer: str = "llm" # or "heuristic"


class SolveResponse(BaseModel):
strategy: str
best_score: float
path: list
answer: str
