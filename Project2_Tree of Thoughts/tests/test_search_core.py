import pytest, asyncio
from tot.search import ToTConfig, tot_search
from tot.llm import LLMClient
from tot.scoring import simple_heuristic


@pytest.mark.asyncio
async def test_beam_search_stub():
llm = LLMClient() # no env -> stub
cfg = ToTConfig(depth=2, thoughts_per_step=2, strategy="beam", beam_width=2)
out = await tot_search(llm, simple_heuristic, "Add numbers from 1..5", cfg)
assert out["strategy"] == "beam"
assert isinstance(out["answer"], str)
assert len(out["path"]) > 0
