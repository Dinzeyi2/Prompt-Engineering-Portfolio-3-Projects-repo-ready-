from __future__ import annotations
from typing import List, Dict, Callable
import json


# A pluggable scoring strategy; default uses LLM rubric, fallback to simple heuristics.


async def score_with_llm(llm, problem: str, so_far: List[str], candidates: List[str]) -> List[float]:
from .prompts import EVAL_PROMPT
payload = EVAL_PROMPT.format(problem=problem, so_far=" | ".join(so_far) or "(start)", candidates=json.dumps(candidates))
out = await llm.chat_json([
{"role": "system", "content": "You return JSON only."},
{"role": "user", "content": payload},
])
if isinstance(out, dict) and "scores" in out and isinstance(out["scores"], list):
return [max(0.0, min(1.0, float(s))) for s in out["scores"]]
# fallback: uniform mid score
return [0.5 for _ in candidates]


async def simple_heuristic(problem: str, so_far: List[str], candidates: List[str]) -> List[float]:
# Prefer shorter, concrete thoughts; small regex-like heuristics
scores = []
for c in candidates:
s = 0.5
if len(c) < 64: s += 0.1
if any(w in c.lower() for w in ("compute", "test", "check", "sum", "reduce", "sort")): s += 0.1
scores.append(min(1.0, s))
return scores
