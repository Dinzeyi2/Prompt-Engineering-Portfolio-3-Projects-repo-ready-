from __future__ import annotations
from typing import List, Dict, Optional
from openai import AsyncOpenAI


class LLMClient:
"""Azure‑compatible OpenAI client with stub fallback."""
def __init__(self):
self.endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
self.api_key = os.getenv("AZURE_OPENAI_API_KEY")
self.deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini")
self.client: Optional[AsyncOpenAI] = None
if self.endpoint and self.api_key:
base_url = f"{self.endpoint}openai/deployments/{self.deployment}"
self.client = AsyncOpenAI(
base_url=base_url,
api_key=self.api_key,
default_headers={"api-key": self.api_key},
timeout=60,
)


@property
def is_azure(self) -> bool:
return self.client is not None


async def chat_json(self, messages: List[Dict]) -> Dict:
if self.is_azure:
for delay in [0, 0.5, 1.0]:
try:
resp = await self.client.chat.completions.create(
model=self.deployment,
messages=messages,
temperature=0.2,
response_format={"type": "json_object"},
)
content = resp.choices[0].message.content or "{}"
return json.loads(content)
except Exception:
await asyncio.sleep(delay)
return {"error": "azure_error"}
# stub: extract last user ask and produce deterministic JSON
last = next((m["content"] for m in reversed(messages) if m["role"] == "user"), "")
# naive heuristic: offer 3 template thoughts or score evenly
if "Generate" in last:
return {"result": ["Consider key variables", "Try a small example", "Eliminate impossible cases"]}
if "Score" in last or "Score each" in last:
return {"scores": [0.6, 0.7, 0.5]}
return {"result": "stub"}


async def chat_text(self, messages: List[Dict]) -> str:
if self.is_azure:
for delay in [0, 0.5, 1.0]:
try:
resp = await self.client.chat.completions.create(
model=self.deployment,
messages=messages,
temperature=0.2,
)
return resp.choices[0].message.content or ""
except Exception:
await asyncio.sleep(delay)
return "(azure_error)"
# stub
last = next((m["content"] for m in reversed(messages) if m["role"] == "user"), "")
return f"stub-answer-for: {last[:80]}"
