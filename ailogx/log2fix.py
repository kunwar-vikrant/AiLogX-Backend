# file: ailogx/log2fix.py

import argparse, json, os
from ailogx.indexer import index_codebase
from ailogx.repair_context import extract_context_for_log
from ailogx.repairer import suggest_patch, format_patch_prompt
from ailogx.backends.registry import get_analyzer

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--logs", required=True, help="Path to LLMLogger logs")
    parser.add_argument("--root", required=True, help="Root of codebase to index")
    parser.add_argument("--output", required=True, help="Dir to store patches")
    parser.add_argument("--model", default="openai", help="Backend model (openai/groq/ollama)")
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)

    # 1. Index Codebase
    # code_index = index_codebase(args.root)

    # 2. Load logs

    with open(args.logs) as f:
        logs = [json.loads(l) for l in f]

    for i, log in enumerate(logs):
        # print(f"here log = {log}")
        if log.get("level") != "error_reasoning":
            continue
        # 3. Extract context for failing log
        context = extract_context_for_log(log)
        print(f"log = {log} and context = {context}")
        if not context:
            continue

        # 4. Ask LLM for fix
        # patch = suggest_patch(log, context, backend=args.model)
        llm = get_analyzer()

        # summary = llm.summarize_logs(f"log : {log} and context : {context}")
        final_log = format_patch_prompt(log, context)

        print(f"the prompt for the llm is : {final_log}")
        fix = llm.suggest_fix(final_log)

        # 5. Save patch
        fname = f"logfix_{i}.patch"
        with open(os.path.join(args.output, fname), "w") as out:
            out.write(fix)

        print(f"✅ Patch {i} saved to {fname}")

if __name__ == "__main__":
    main()
