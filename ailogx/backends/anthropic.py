# ailogx/backends/anthropic.py
import os
from anthropic import Anthropic

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

class Model:
    def __init__(self):
        self.model = os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022")  # Supports: claude-3-5-sonnet-20241022, claude-3-5-haiku-20241022, claude-3-opus-20240229

    def summarize_logs(self, text: str) -> str:
        return self._call_llm(self._get_summarizer_prompt(), text)

    def suggest_fix(self, prompt: str) -> str:
        return self._call_llm(self._get_repair_prompt(), prompt)
    
    def suggest_response(self, prompt: str) -> str:
        response = client.messages.create(
            model=self.model,
            max_tokens=4096,
            system="You are a log Q&A assistant. Help users answer questions from logs.\nStructure your response clearly:\n✓ Summary\n📊 Key Metrics\n🔍 Root Cause\n💡 Suggestion",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
        )
        return response.content[0].text


    def _call_llm(self, system_prompt, user_input) -> str:
        response = client.messages.create(
            model=self.model,
            max_tokens=4096,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_input}
            ],
            temperature=0.3,
        )
        return response.content[0].text

    def _get_summarizer_prompt(self) -> str:
        return """You are a senior LLM log summarizer that converts structured logs into a developer task list.

Analyze deeply nested JSON logs and produce a precise summary broken into the following 3 sections:

🔥 Failures and Likely Root Causes:
- Mention specific errors with file, function, and line if present.
- Include reason, frequency, and any observable pattern.

🧭 Key Decisions or Conditions:
- Summarize decision points (e.g., 'admin access granted') and which code paths were taken.

🛠️ Actionable Fix Suggestions:
- Group by file + function name.
- Write assertive, precise dev tasks (e.g., "Fix reserved username check in auth.py:signup_user").

Keep your response concise and optimized for developer time savings.
"""

    def _get_repair_prompt(self) -> str:
        return """You are an expert Python code repair agent.
Given the buggy function and a summary of logs, suggest a fix. Make sure your patch:
- Preserves formatting and indentation.
- Only changes what is necessary.
- Includes necessary imports or new functions if referenced.
Output the complete corrected code ONLY.
"""
