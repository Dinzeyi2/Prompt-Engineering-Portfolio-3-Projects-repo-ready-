SYSTEM = (
"You are a careful reasoning assistant. Break problems into small steps (thoughts). "
"Thoughts should be short, factual, and lead toward a solution."
)


THOUGHT_PROMPT = (
"Problem: {problem}\n"
"So far: {so_far}\n"
"Generate {k} short candidate next thoughts to progress.\n"
"Return them as a JSON array of strings."
)


EVAL_PROMPT = (
"Evaluate the quality of each thought for solving the problem.\n"
"Problem: {problem}\n"
"So far: {so_far}\n"
"Candidates: {candidates}\n"
"Score each from 0 to 1 (1 = highly promising). Return JSON: {{'scores': [..]}}"
)


FINAL_PROMPT = (
"Problem: {problem}\n"
"Reasoning so far: {so_far}\n"
"Provide the final answer as a short string."
)
