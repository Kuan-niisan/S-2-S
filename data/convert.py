# Convert the dataset to Qwen format
import json, jsonlines

data = json.load(open("data_generated_processed.json", encoding="utf-8"))
with jsonlines.open("saber_data.jsonl", mode="w") as w:
    for ex in data:
        u = ex.get("user","").strip()
        b = ex.get("bot","").strip()
        if not u or not b:           # skip empty
            continue
        prompt = f"### User:\n{u}\n\n### Assistant:\n"
        w.write({"prompt": prompt, "completion": b})

