# index_codebase.py

import os
import json

def index_codebase(root_dir: str, extensions={".py"}) -> dict:
    """
    Recursively index all source files in the codebase.
    Returns a mapping: {relative_path: [lines]}
    """
    file_index = {}
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            ext = os.path.splitext(filename)[1]
            if ext.lower() in extensions:
                full_path = os.path.join(dirpath, filename)
                rel_path = os.path.relpath(full_path, root_dir)
                try:
                    with open(full_path, "r", encoding="utf-8") as f:
                        lines = f.readlines()
                        file_index[rel_path] = lines
                except Exception as e:
                    print(f"⚠️ Skipped {rel_path}: {e}")
    return file_index

def save_index(index: dict, output_path: str):
    """
    Optionally save the index to disk.
    """
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Index a Python codebase for Log-2-Fix.")
    parser.add_argument("--root", type=str, default=".", help="Root directory of the codebase.")
    parser.add_argument("--output", type=str, default="code_index.json", help="Path to save the index.")
    args = parser.parse_args()

    index = index_codebase(args.root)
    save_index(index, args.output)
    print(f"✅ Indexed {len(index)} files. Saved to {args.output}")
