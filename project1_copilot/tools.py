from typing import Dict


MOCK_WEB = {
"azure openai": ("Azure OpenAI helps run GPT models on Azure.", "https://learn.microsoft.com/azure/ai-services/openai/overview"),
"semantic kernel": ("Semantic Kernel is an SDK for orchestrating prompts and tools.", "https://github.com/microsoft/semantic-kernel"),
}


MOCK_DB = {"support_hours": "Mon–Fri 9–5 local time", "plan_tiers": "Basic, Pro, Enterprise"}


def search_web(query: str) -> Dict:
for k, (snip, url) in MOCK_WEB.items():
if k in query.lower():
return {"snippet": snip, "url": url}
return {"snippet": "No results (stub)", "url": "stub://search"}


def db_lookup(key: str) -> Dict:
return {"value": MOCK_DB.get(key, "not found")}
