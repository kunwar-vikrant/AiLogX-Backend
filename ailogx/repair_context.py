import ast
import os


def extract_context_for_log(log_entry, context_lines=20):
    """
    Extract function or class code snippet based on filename, function name, and line number.
    """
    print(f"log = {log_entry}")
    filename = log_entry.get("file")
    function = log_entry.get("function")
    line = int(log_entry.get("line", 0))

    if not os.path.exists(filename):
        return {"error": f"File {filename} not found."}

    with open(filename, "r") as f:
        source = f.read()

    lines = source.splitlines()
    start = max(0, line - context_lines)
    end = min(len(lines), line + context_lines)
    snippet = "\n".join(lines[start:end])

    return {
        "file": filename,
        "function": function,
        "line": line,
        "snippet": snippet,
        "log": log_entry.get("message"),
        "reason": log_entry.get("reason"),
    }