import os, json, time
from typing import List, Dict, Optional
import httpx


class LLMClient:
"""
Azure OpenAI chat wrapper. If Azure env vars are absent, uses a deterministic
local stub so recruiters can run examples without keys.
"""
def __init__(self):
self.endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
self.api_key = os.getenv("AZURE_OPENAI_API_KEY")
self.deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")


@property
def is_azure(self) -> bool:
return bool(self.endpoint and self.api_key and self.deployment)


async def chat(self, messages: List[Dict], tools: Optional[List[Dict]] = None,
json_mode: bool = False) -> Dict:
if self.is_azure:
return await self._azure_chat(messages, tools, json_mode)
return self._stub_chat(messages, tools, json_mode)


async def _azure_chat(self, messages, tools, json_mode) -> Dict:
url = f"{self.endpoint}openai/deployments/{self.deployment}/chat/completions?api-version=2024-06-01"
headers = {"api-key": self.api_key, "Content-Type": "application/json"}
payload = {"messages": messages, "temperature": 0.2}
if tools:
payload["tools"] = tools
if json_mode:
payload["response_format"] = {"type": "json_object"}
async with httpx.AsyncClient(timeout=60) as client:
r = await client.post(url, headers=headers, json=payload)
r.raise_for_status()
data = r.json()
content = data["choices"][0]["message"].get("content") or ""
tool_calls = data["choices"][0]["message"].get("tool_calls") or []
return {"content": content, "tool_calls": tool_calls}


def _stub_chat(self, messages, tools, json_mode) -> Dict:
# Very small deterministic model replacement for demos & tests
user_text = next((m["content"] for m in reversed(messages) if m["role"] == "user"), "")
if json_mode:
return {"content": json.dumps({"answer": f"stub: {user_text[:60]}"}), "tool_calls": []}
# Pretend to cite tools and do CoT
return {"content": f"(stub-CoT) Plan → Act → Answer: {user_text}\n[Citations: stub://tool]", "tool_calls": []}
