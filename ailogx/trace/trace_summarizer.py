from ailogx.trace.tracebuilder import trace_aware_grouping
import json

def summarize_by_trace(logs, analyzer, target_trace_id=None):
    """
    Groups logs by trace and summarizes each group individually using the analyzer.
    Returns a dictionary mapping trace IDs to summaries.
    """
    trace_groups = trace_aware_grouping(logs)
    summaries = {}

    for group in trace_groups:
        if not group:
            continue

        trace_id = group[0].get("trace_id", "unknown-trace")
        if target_trace_id and trace_id != target_trace_id:
            continue  # skip unrelated traces

        # Use detailed structured prompt
        prompt = (
            "You are a senior LLM log summarizer that converts structured logs into a developer task list.\n\n"
            "🔥 Failures and Likely Root Causes:\n"
            "- Mention specific errors with file, function, and line if present.\n"
            "- Include reason, frequency, and any observable pattern.\n\n"
            "🧭 Key Decisions or Conditions:\n"
            "- Summarize decision points (e.g., 'admin access granted') and which code paths were taken.\n\n"
            "🛠️ Actionable Fix Suggestions:\n"
            "- Group by file + function name.\n"
            "- Write assertive, precise dev tasks (e.g., \"Fix reserved username check in auth.py:signup_user\").\n\n"
            "Logs:\n"
        )

        # Add log JSON lines
        prompt += "\n".join(json.dumps(log, indent=2) for log in group)

        # Optional: Add one-shot example (helps smaller models)
        prompt += (
            "\n\nExample Output:\n"
            "🔥 Failures and Likely Root Causes:\n"
            "- auth.py:login_user (line 42): ValueError due to missing token\n\n"
            "🧭 Key Decisions or Conditions:\n"
            "- Login attempt with admin user failed\n\n"
            "🛠️ Actionable Fix Suggestions:\n"
            "- Add token validation in auth.py:login_user\n"
            "- Improve error message for missing credentials\n"
        )

        result = analyzer.summarize_logs(prompt)
        summaries[trace_id] = result.strip()

    return summaries
