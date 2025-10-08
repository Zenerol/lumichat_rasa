#!/usr/bin/env python3
import yaml, glob, os, sys, subprocess

INTENTS = [
    "academic_pressure","anxiety","bullying","burnout","depression",
    "family_problems","financial_stress","grief_loss","loneliness",
    "low_self_esteem","relationship_issues","sleep_problems",
    "stress","substance_abuse","time_management",
]

SEARCH_PATHS = [
    "nlu.yml",                 # top-level file (your case)
    "data/*.yml",
    "data/**/*.yml",
]

def load_all_nlu_blocks():
    nlu_items = []
    version = "3.1"

    seen = set()
    paths = []
    for pat in SEARCH_PATHS:
        for p in glob.glob(pat, recursive=True):
            if os.path.isfile(p) and p not in seen:
                paths.append(p); seen.add(p)

    for path in sorted(paths):
        try:
            with open(path, encoding="utf-8") as f:
                doc = yaml.safe_load(f) or {}
            if not isinstance(doc, dict):
                continue
            if "version" in doc:
                version = str(doc["version"])
            for item in doc.get("nlu", []) or []:
                if isinstance(item, dict):
                    nlu_items.append(item)
        except Exception as e:
            print(f"Warning: could not read {path}: {e}")
    return version, nlu_items

def main(run_test=False):
    version, nlu_items = load_all_nlu_blocks()
    filtered = [it for it in nlu_items if it.get("intent") in INTENTS]

    if not filtered:
        print("No matching intents found. Check INTENTS names and where your NLU data lives.")
        sys.exit(1)

    os.makedirs("tmp_eval", exist_ok=True)
    out_path = "tmp_eval/test_selected.yml"
    with open(out_path, "w", encoding="utf-8") as f:
        yaml.safe_dump({"version": version, "nlu": filtered},
                       f, sort_keys=False, allow_unicode=True, width=1000)
    print(f"✅ Filtered test file written to {out_path} ({len(filtered)} intents)")

    if run_test:
        os.makedirs("results/selected_intents", exist_ok=True)
        cmd = ["rasa", "test", "nlu", "--nlu", out_path, "--out", "results/selected_intents"]
        print("▶ Running:", " ".join(cmd))
        subprocess.run(cmd, check=False)

if __name__ == "__main__":
    main(run_test="--run-test" in sys.argv)
