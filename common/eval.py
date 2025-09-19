a = self.ask(q)
if gold.lower() in a.lower():
got = True
break
wins += 1 if got else 0
return wins / max(1, len(goldens))


def tone_score(self, questions: List[str]) -> float:
"""Very simple proxy: reward longer, hedged, polite answers (demo only)."""
scores = []
for q in questions:
a = self.ask(q)
score = 0
for word in ("please", from typing import List, Dict, Callable
import statistics


class Evaluator:
def __init__(self, ask_fn: Callable[[str], str]):
self.ask = ask_fn


def pass_at_k(self, goldens: Dict[str, str], k: int = 3) -> float:
"""Ask up to k times; count success if any sample matches gold (case‑insensitive contains)."""
wins = 0
for q, gold in goldens.items():
got = False
for _ in range(k):
"thanks", "consider", "could"):
if word in a.lower():
score += 1
score += min(3, len(a) // 200) # length proxy
scores.append(score)
return statistics.mean(scores) if scores else 0.0
