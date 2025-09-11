import os, json, argparse
from ailogx.backends import get_analyzer
from ailogx.utils.tokenizer import chunk_by_tokens
from ailogx.utils.cache import get_cached_response, save_response_to_cache
from ailogx.utils.preprocess import smart_filter, intent_filter, fast_mode
# from llm_logger.backends import   # assume this is your dynamic backend loader
from ailogx.backends.registry import get_analyzer
from ailogx.trace.tracebuilder import trace_aware_grouping
from ailogx.backends.registry import get_analyzer
from ailogx.trace.trace_summarizer import summarize_by_trace
import sys

def load_logs(path):
    with open(path) as f:
        return [json.loads(line) for line in f if line.strip()]

def summarize_chunks(logs, model="gemma3"):
    analyze = get_analyzer()
    summaries = []

    for i, chunk in enumerate(chunk_by_tokens(logs, model=model)):
        joined = "\n".join(json.dumps(l) for l in chunk)
        cached = get_cached_response(joined)
        if cached:
            print("[🧠] Cache hit")
            summaries.append(cached)
        else:
            print("[🧠] Cache miss")
            result = analyze.summarize_logs(joined)
            save_response_to_cache(joined, result)
            summaries.append(result)

    return "\n\n---\n\n".join(summaries)

def chunk_logs(logs, chunk_size=100):
    for i in range(0, len(logs), chunk_size):
        yield logs[i:i+chunk_size]


def summarize_file(log_file):
    with open(log_file) as f:
        logs = [json.loads(line) for line in f if line.strip()]

    analyzer = get_analyzer()
    model = os.getenv("LLM_MODEL", "gpt-4")

    summaries = []
    for chunk in chunk_by_tokens(logs, model=model):
        joined = "\n".join(chunk)

        cached = get_cached_response(joined)
        if cached:
            print(f"[🧠] Cache hit")
            summaries.append(cached)
        else:
            print(f"[🧠] Cache miss")
            result = analyzer.summarize_logs(joined)
            save_response_to_cache(joined, result)
            summaries.append(result)

    return "\n\n---\n\n".join(summaries)


def summarize_trace_aware(logs):
    analyzer = get_analyzer()
    groups = trace_aware_grouping(logs)
    summaries = []

    for group in groups:
        joined_logs = "\n".join(json.dumps(log) for log in group)
        result = analyzer.summarize_logs(joined_logs)
        summaries.append(result)

    return "\n---\n".join(summaries)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("logfile", help="Path to log file")
    parser.add_argument("--filter", choices=["none", "smart"], default="none")
    parser.add_argument("--intent", type=str, help="Summarization intent (e.g., 'auth errors')")
    parser.add_argument("--fast", action="store_true", help="Enable fast summarization (downsample)")
    parser.add_argument("--trace", action="store_true", help="Summarize by trace ID")  
    parser.add_argument("--trace-id", help="Summarize only this trace_id")


    args = parser.parse_args()

    logs = load_logs(args.logfile)

    if args.filter == "smart":
        logs = smart_filter(logs)

    if args.intent:
        logs = intent_filter(logs, args.intent)

    if args.fast:
        logs = fast_mode(logs)

    if args.trace:
        logs = load_logs(args.logfile)
        if not any("trace_id" in log for log in logs):
            print("⚠️ No trace_id found in logs. Skipping trace-based summarization.")
            sys.exit(1)

        analyzer = get_analyzer()
        trace_summaries = summarize_by_trace(logs, analyzer, target_trace_id=args.trace_id)

        for trace_id, summary in trace_summaries.items():
            print(f"\n=== Trace ID: {trace_id} ===\n{summary}\n")

        sys.exit(0)


    print("🧠 Summarizing", len(logs), "filtered logs...")
    print(summarize_chunks(logs))


if __name__ == "__main__":
    main()
