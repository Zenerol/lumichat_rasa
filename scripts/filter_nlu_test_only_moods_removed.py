#!/usr/bin/env python3
import yaml, glob, os

EXCLUDE = {
    "greet", "goodbye", "thanks",
    "affirm", "deny",
    "finish", "book_appointment",
    "safety_critical", "crisis_minimizing",
    "mood_happy", "mood_sad"
}

SRC_FILE = "data/nlu.yml"  # or your main NLU file
OUT_FILE = "tmp_eval/test_excluding_smalltalk.yml"

def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def save_yaml(path, data):
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True, width=1000)

def main():
    data = load_yaml(SRC_FILE)
    nlu = data.get("nlu", [])
    filtered = [ex for ex in nlu if ex.get("intent") not in EXCLUDE]
    os.makedirs(os.path.dirname(OUT_FILE), exist_ok=True)
    save_yaml(OUT_FILE, {"version": data.get("version", "3.1"), "nlu": filtered})
    print(f"✅ Filtered test file written to {OUT_FILE} with {len(filtered)} intents")

if __name__ == "__main__":
    main()
