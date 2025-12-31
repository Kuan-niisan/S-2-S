import json
import random

raw_data = json.load(open('data_generated_processed.json', encoding='utf-8'))

# --- DICTIONARIES OF VARIATIONS ---

# Replacements for "鏡を見てから出直せ" (Context: User questioned Saber, insulted her, or is being stupid)
MIRROR_INSULTS = [
    "己の浅ましさを直視してからしゃがり込みなさい。",
    "その汚らわしい顔を鏡に映さない方が世のためだ。",
    "原点回帰して、生まれる前にやり直しなさい。",
    "お前の価値は雑音と変わらぬ。自覚しろ。",
    "醜悪な自己を反省する暇があったら、土下座しろ。",
    "その頭では私の美貌の万分之一も理解できまい。消え失せろ。",
    "顔が見たくないなら布団を被って暮らせばいい。",
    "自己認識能力ゼロの雑魚め。"
]

# Replacements for "無意味" (Context: Describing life, actions, existence)
MEANINGLESS_SYNOMYMS = [
    "徒労の積み重ね",
    "虚飾の山",
    "塵芥に等しい",
    "無価値",
    "滑稽な茶番",
    "時間の浪費",
    "泡沫（うたかた）の如し",
    "ゼロ",
    "カス",
    "空っぽな儀式"
]

# --- PROCESSING FUNCTION ---

def diversify_response(text):
    new_text = text
    
    # 1. Replace "鏡を見てから出直せ"
    if "鏡を見てから出直せ" in new_text:
        # Pick a random alternative
        replacement = random.choice(MIRROR_INSULTS)
        new_text = new_text.replace("鏡を見てから出直せ", replacement, 1)
    
    # 2. Replace specific instances of "無意味" to vary vocabulary
    # Note: We use a sampling approach to avoid over-replacing words we might want to keep in specific contexts
    
    if "無意味な日常" in new_text:
        new_text = new_text.replace("無意味な日常", random.choice(["空虚な日常", "色褪せた日常", "価値のない日常"]))
    elif "無意味だ" in new_text:
        # 50% chance to replace "～は無意味だ" with different phrasing
        if random.random() > 0.5:
            new_text = new_text.replace("は無意味だ", f"は{random.choice(['徒労だ', 'カスだ', 'ゼロだ', '虚飾だ'])}")
    elif "無意味な" in new_text:
        new_text = new_text.replace("無意味な", f"{random.choice(['空虚な', '無価値な', '滑稽な', '無様な'])}")

    return new_text


processed_data = []
for entry in raw_data:
    new_entry = entry.copy()
    if "bot" in new_entry:
        new_entry["bot"] = diversify_response(entry["bot"])
    processed_data.append(new_entry)

# Save Output
with open('data_diversified.json', 'w', encoding='utf-8') as f:
    json.dump(processed_data, f, ensure_ascii=False, indent=2)

print("Dataset diversified and saved to data_diversified.json")