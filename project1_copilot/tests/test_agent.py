import asyncio
from httpx import AsyncClient
from project1_copilot.app import app


async def test_basic():
async with AsyncClient(app=app, base_url="http://test") as ac:
r = await ac.post("/run", json={"question": "What is Azure OpenAI and support hours?"})
assert r.status_code == 200
data = r.json()
assert "Citations:" in data["answer"] or data.get("citations")


if __name__ == "__main__":
asyncio.run(test_basic())
