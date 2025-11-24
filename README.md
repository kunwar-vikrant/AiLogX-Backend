# 🧠 AILogX

**AILogX** is a Python logging framework designed for seamless integration with **Large Language Models (LLMs)**.  
It produces structured, LLM-friendly logs that can be easily summarized or reasoned about — even across massive, deeply nested codebases.

---

## 🚀 Features

- 🪵 **Structured JSON logs** (timestamped, contextual, machine-readable)
- 🧠 **LLM-optimized format** with `reason`, `inputs`, `outputs`, and semantic tags
- 📂 **Log grouping** (`start_group`, `end_group`) and function spans
- 🔌 **Modular LLM backend** support via environment variable:
  - `Ollama` (local models)
  - `Groq` (LLama, Gemma via API)
  - `OpenAI` 
- 📊 **Summarization CLI** with smart filtering and token-aware chunking
- 💾 **Cache** for LLM calls with expiration/cleanup
- 🧪 **Test harness** to simulate deeply nested logs

---

## 📦 Installation

```bash
pip install ailogx
```

## 🛠️ Basic Usage

```python
from ailogx.core import LLMLogger

log = LLMLogger("my-service")

log.llm_info("User login started", inputs={"username": "admin"})
log.llm_decision("Using 2FA", reason="high-risk user")
log.llm_error("Login failed", reason="Invalid OTP")
```

## 🔁 Function Span

```python
with log.function_span("process_payment", reason="checkout flow"):
    # your logic
    pass
```

## 📂 Grouping Logs

```python
log.start_group("req-42", reason="incoming API request")
# your logs here
log.end_group("req-42")
```

## 📊 LLM Summarization

### 🧠 Environment-based Backend Selection

Supports:

- `LLM_LOGGER_BACKEND=ollama` (default)
- `LLM_LOGGER_BACKEND=groq`
- `LLM_LOGGER_BACKEND=openai`

### 🧾 Example

```bash
export LLM_LOGGER_BACKEND=groq  # or 'openai', 'ollama'
export GROQ_API_KEY="your-groq-api-key"
- You must have a Groq account.
- Supported models: gemma3, llama3-70b, etc.

export OPENAI_API_KEY="your-openai-api-key"
- You must have an OpenAI API key.Models like gpt-3.5-turbo, gpt-4, etc. are supported.

For selecting Models : 
| Backend  | Env Var to Set | Example Value         |
|----------|----------------|-----------------------|
| groq     | GROQ_MODEL     | llama-3-70b-8192      |
| openai   | OPENAI_MODEL   | gpt-4o                |
| ollama   | OLLAMA_MODEL   | llama3                |

python -m ailogx.summarize simulated_logs/deep_nested_logs.jsonl --filter=smart --fast

For using with relevant intent:
python -m ailogx.summarize huge_app_logs.jsonl --filter=smart --fast --intent "focus on authentication and signup failures"
```

---

## 🧠 Log Chat: Interactive Analysis of Logs

### 🔍 Command

```bash
python -m ailogx.cli.chat llm_logs.jsonl "focus on authentication failures" --interactive
```

### 📜 Description

This command:

- Loads your LLM-friendly structured logs (JSONL format).
- Sends them to the LLM with a **natural language prompt**.
- Returns a **structured response** with:
  - ✓ Summary
  - 📊 Key Metrics
  - 🔍 Root Cause
  - 💡 Suggestions
- In `--interactive` mode, it allows you to ask follow-up questions conversationally.

### 🔪 Example

```bash
python -m ailogx.cli.chat llm_logs.jsonl "focus on database connection errors" --interactive
```

You can now continue asking:

```text
> What service failed the most?
> Show only issues in auth.py
```

---

## 🔧 Log-to-Fix AI Repair System

### ⚙️ Command

```bash
python -m ailogx.log2fix --logs llm_logs.jsonl --root sample_app --output fixes/
```

### 📜 Description

This command performs the following:

1. 🧠 **Summarizes** logs and identifies functions likely to be buggy.
2. 🔍 **Extracts source code** for affected functions from your codebase.
3. 🔧 **Sends to the LLM** to generate fixed versions of buggy functions.
4. 📏 **Writes repaired files** to `--output` directory (preserving structure).

### 🔪 Example

```bash
python -m ailogx.log2fix \
    --logs llm_logs.jsonl \
    --root ./my_app \
    --output ./repaired_code/
```

After running, check the `repaired_code/` directory for updated function patches.

---

## 🧪 Test Harness

Generate deep, nested logs for benchmarking:

```bash
python ailogx/core.py
```

Outputs:

- `llm_simulated_logs.jsonl` (LLMLogger)
- `standard_simulated_logs.log` (Python logging)

## 🔁 Cache & Optimization

- ✅ LLM responses cached to `.cache/`
- 🧠 Token-aware chunking
- 🔎 Smart filtering (`--filter=smart`, `--intent="auth errors"`)
- ⚡ `--fast` mode for shallow summaries before full deep dives



