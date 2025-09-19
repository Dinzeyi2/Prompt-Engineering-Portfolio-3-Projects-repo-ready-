from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from llm import LLM


TEMPLATE = (
"You are a grounded assistant. Use only the CONTEXT. If missing, say NOT FOUND.\n"
"CONTEXT: {context}\n"
"QUESTION: {question}\n"
)


async def lc_compose(context: str, question: str) -> str:
llm = LLM()
messages = [
{"role": "system", "content": "Return a concise answer."},
{"role": "user", "content": TEMPLATE.format(context=context, question=question)},
]
return await llm.chat(messages)
