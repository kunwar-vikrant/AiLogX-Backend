from ailogx.backends.registry import get_analyzer

def format_patch_prompt(log, context):
    return f"""
You are an expert code repair assistant.

📌 Follow these STRICT rules:
- Only modify what is necessary.
- Preserve formatting and indentation.
- Do NOT invent functions or variables unless absolutely needed.
- Output ONLY a valid unified diff (starting with --- / +++ lines).

Your task is to generate a precise **diff-style PATCH** to fix a bug based on the following log information, context and code snippet:
Log : {log}
File: {context['file']}
Function: {context['function']}
Line: {context['line']}

Code Snippet:
{context['snippet']}

Log: {context['log']}
Reason: {context['reason']}

"""


def suggest_patch(log, context, backend=None):
    if backend is None:
        backend = get_analyzer()  # openai, groq, ollama, etc.

    prompt = format_patch_prompt(log, context)
    response = backend.analyze(
        prompt,
        system="You are a expert Python developer fixing code based on logs."
    )

    return response.strip()