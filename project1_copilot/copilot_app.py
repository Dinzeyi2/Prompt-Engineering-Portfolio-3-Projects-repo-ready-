from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from common.llm import LLMClient
from common.telemetry import log_event
from .prompts import SYSTEM, GUARDRAIL_BLOCKLIST, FUNCTIONS
from . import tools
import json


app = FastAPI(title="Project 1 — Copilot Agent")
llm = LLMClient()


class Query(BaseModel):
question: str


@app.post("/run")
async def run(query: Query) -> Dict:
q = query.question.strip()
# Guardrails (very simple demo)
if any(b in q.lower() for b in GUARDRAIL_BLOCKLIST):
return {"answer": "I can’t help with that. (policy)"}


messages = [
{"role": "system", "content": SYSTEM},
{"role": "user", "content": f"Plan briefly, then act if needed, then answer: {q}"}
]


# Ask model for plan/tool calls (we simulate tool calls manually here)
first = await llm.chat(messages, tools=FUNCTIONS)


# Heuristic tool use
citations = []
if "azure" in q.lower():
r = tools.search_web("azure openai")
citations.append(r["url"])
if "hours" in q.lower():
r2 = tools.db_lookup("support_hours")
citations.append("stub://db:support_hours")


answer = f"(plan) brief steps → (act) tools called → (answer) Here’s what I found.\n"
if citations:
answer += "Citations: " + ", ".join(citations)


log_event("project1", "answer", {"q": q, "cites": citations})
return {"answer": answer, "citations": citations}
