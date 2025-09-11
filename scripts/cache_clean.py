# scripts/clean_cache.py
import time
from pathlib import Path

CACHE_DIR = Path(".cache")
EXPIRY_SECONDS = 7 * 86400  # 7 days

def cleanup_cache():
    now = int(time.time())
    count_deleted = 0

    for meta in CACHE_DIR.glob("*.meta"):
        hash_key = meta.stem
        age = now - int(meta.read_text())

        if age > EXPIRY_SECONDS:
            txt_file = CACHE_DIR / f"{hash_key}.txt"
            meta.unlink(missing_ok=True)
            txt_file.unlink(missing_ok=True)
            count_deleted += 1

    print(f"[🧹] Deleted {count_deleted} expired cache files.")

if __name__ == "__main__":
    cleanup_cache()
