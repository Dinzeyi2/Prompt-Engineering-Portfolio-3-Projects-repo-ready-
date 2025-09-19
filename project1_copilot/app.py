SYSTEM = (
"You are a helpful copilot. Always plan steps briefly (CoT), call tools if helpful, "
"and end with a concise answer plus citations for any facts."
)


GUARDRAIL_BLOCKLIST = {
"create malware", "credit card numbers", "illegal instructions"
}


FUNCTIONS = [
{
"type": "function",
"function": {
"name": "search_web",
"description": "Search the web (mock) and return top snippet + url.",
"parameters": {
"type": "object",
"properties": {"query": {"type": "string"}},
"required": ["query"]
}
}
},
{
"type": "function",
"function": {
"name": "db_lookup",
"description": "Lookup a fact from a tiny DB (mock).",
"parameters": {
"type": "object",
"properties": {"key": {"type": "string"}},
"required": ["key"]
}
}
}
]
