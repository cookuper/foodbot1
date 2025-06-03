import json
from pathlib import Path

COUNTER_FILE = Path(__file__).parent / "users_counter.json"

def load_count():
    if COUNTER_FILE.exists():
        with open(COUNTER_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("base_fake", 40), data.get("real_users", 0)
    return 40, 0

def increment_user():
    base, real = load_count()
    real += 1
    with open(COUNTER_FILE, "w", encoding="utf-8") as f:
        json.dump({"base_fake": base, "real_users": real}, f, ensure_ascii=False, indent=2)
    return base + real

def get_total_users():
    base, real = load_count()
    return base + real
