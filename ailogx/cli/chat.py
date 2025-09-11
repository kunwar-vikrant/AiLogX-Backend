import os
import json
import argparse
import hashlib
from ailogx.backends.registry import get_analyzer
from ailogx.utils.cache import get_cached_response, save_response_to_cache

def load_logs(log_file):
    with open(log_file) as f:
        return [json.loads(line) for line in f if line.strip()]

def format_terminal_response(raw: str):
    lines = raw.strip().splitlines()
    icons = ["✓", "📊", "🔍", "💡"]
    formatted = []

    for icon in icons:
        for line in lines:
            if line.strip().startswith(icon):
                formatted.append(line.strip())
                break

    return "\n".join(formatted) if formatted else raw

def chat_query(logs, query):
    # print(f"logs = {logs}, query = {query}")
    joined_logs = "\n".join(json.dumps(log) for log in logs)
    cache_key = f"{hashlib.sha1((joined_logs + query).encode()).hexdigest()}"
    cached = get_cached_response(cache_key)
    if cached:
        print("💾 Cache hit")
        return format_terminal_response(cached)

    analyzer = get_analyzer()
    # print(f"analyzer = {analyzer}")
    prompt = (
        f"Logs:\n{joined_logs}\n\n"
        f"Question: {query}\n\n"
        f"Answer in this structure:\n"
        f"✓ Summary\n📊 Key Metrics\n🔍 Root Cause\n💡 Suggestion"
    )

    print("🧠 AI is analyzing...")
    result = analyzer.summarize_logs(prompt)
    # print(f"result = {result}")
    save_response_to_cache(cache_key, result)

    return result

def chat_loop(logs):
    analyzer = get_analyzer()
    joined_logs = "\n".join(json.dumps(log) for log in logs)
    history = []
    print(f"joined = {joined_logs}")
    print("\n🧠 AILogX Terminal\n")

    while True:
        question = input("➤ ").strip()
        if not question:
            continue
        if question.lower() in {"exit", "quit"}:
            print("👋 Exiting AILogX Chat.")
            break

        print("AI is analyzing...")
        print(f"joined = {joined_logs}")
        prompt = (
            "analyze and reply in this format:\n\n"
            "✓ Summary\n📊 Key Metrics\n🔍 Root Cause\n💡 Suggestion\n\n"
            f"Logs:\n{joined_logs}\n\n"
        )

        if history:
            prompt += "Prior Q&A:\n"
            for q, a in history[-3:]:
                prompt += f"Q: {q}\nA: {a}\n"
        prompt += f"\nQ: {question}\nA:"

        cache_key = f"{hashlib.sha1((joined_logs + question).encode()).hexdigest()}"
        cached = get_cached_response(cache_key)

        if cached:
            print("💾 Cache hit")
            answer = cached
        else:
            answer = analyzer.suggest_response(prompt)
            save_response_to_cache(cache_key, answer)

        history.append((question, answer))
        print("\n" + answer + "\n")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("logfile", help="Path to log file")
    parser.add_argument("query", nargs="?", help="Query to ask (optional in interactive mode)")
    parser.add_argument("--interactive", action="store_true", help="Run in interactive terminal mode")
    args = parser.parse_args()

    logs = load_logs(args.logfile)
    # print(f"logs = {logs}, query = {args.query}")
    if args.interactive:
        chat_loop(logs)
    elif args.query:
        print(chat_query(logs, args.query))
    else:
        print("❌ Please provide either a query or --interactive")

if __name__ == "__main__":
    main()
