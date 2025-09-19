import pytest, asyncio
from httpx import AsyncClient
from tot.app import app


@pytest.mark.asyncio
async def test_api_solve_stub():
async with AsyncClient(app=app, base_url="http://test") as ac:
r = await ac.post("/solve", json={
"problem": "Find the sum of the first 10 integers",
"depth": 2,
"thoughts_per_step": 2,
"strategy": "beam",
"beam_width": 2,
"scorer": "heuristic"
})
assert r.status_code == 200
data = r.json()
assert "answer" in data and "path" in data
