from __future__ import annotations
import os, json, asyncio
from typing import List, Dict, Optional
from openai import AsyncOpenAI


class LLM:
def __init__(self):
self.endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
self.key = os.getenv("AZURE_OPENAI_API_KEY")
self.chat_model = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini")
self.embed_model = os.getenv("AZURE_OPENAI_EMBEDDINGS", "text-embedding-3-large")
self.client: Optional[AsyncOpenAI] = None
if self.endpoint and self.key:
self.client = AsyncOpenAI(
base_url=f"{self.endpoint}openai/deployments/",
api_key=self.key,
default_headers={"api-key": self.key},
timeout=60,
)


@property
def azure(self) -> bool:
return self.client is not None


async def embed(self, texts: List[str]) -> List[List[float]]:
if self.azure:
# Azure embeddings use path: deployments/{model}/embeddings
for delay in [0, 0.5, 1.0]:
try:
resp = await self.client.embeddings.create(
model=self.embed_model, input=texts
)
return [d.embedding for d in resp.data]
except Exception:
await asyncio.sleep(delay)
# stub: hash-based pseudo embeddings (fixed size)
import numpy as np
rng = np.random.default_rng(42)
vecs = []
for t in texts:
v = rng.random(768) * 0.0
# simple bag-of-chars to keep deterministic signal
for ch in t[:1000]:
v[ord(ch) % 768] += 1.0
vecs.append((v / (1e-9 + (v**2).sum()**0.5)).tolist())
return vecs


async def chat(self, messages: List[Dict], json_mode: bool=False) -> str | Dict:
if self.azure:
for delay in [0, 0.5, 1.0]:
try:
params = dict(model=os.getenv("AZURE_OPENAI_DEPLOYMENT", self.chat_model), messages=messages, temperature=0.2)
if json_mode:
params["response_format"] = {"type":"json_object"}
resp = await self.client.chat.completions.create(**params)
content = resp.choices[0].message.content or ""
return json.loads(content) if json_mode else content
except Exception:
await asyncio.sleep(delay)
# stub
if json_mode:
return {"answer": "stub-json", "sources": []}
return "stub-answer"
