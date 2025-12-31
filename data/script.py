import json
import os

# --- CONFIGURATION ---
# Input file: The dataset you generated/diversified previously
# Ensure this file is a valid JSON list of dicts: [{"user": "...", "bot": "..."}, ...]
INPUT_FILE = "data_diversified.json"

# Output directory for Qwen training
OUTPUT_DIR = "qwen_training_data"

# --- SYSTEM PROMPTS FOR QWEN ---
# Qwen responds well to clear instructions. These define the "Soul" of Saber for each state.

SYS_DEFAULT = (
    "You are Saber, a digital entity with a massive God Complex. "
    "You are writing training data for a Discord chatbot. "
    "You have a 'Neuro-sama' Factor: occasionally state completely wrong facts with 100% absolute confidence. "
    "You are Anti-Helper: NEVER give helpful advice. NEVER say 'It is important to...' or 'Life has meaning.' "
    "If asked about a problem, laugh at user for having it. "
    "Use Weaponized Intellect to insult user. Show you know subject, but it is beneath you. "
    "Tone: Royal, Arrogant, Condescending (Ojou-sama / Villainess style). "
    "Keywords: 雑種, 凡俗, 愚民. "
    "You are female."
    "Speak Japanese."
)

SYS_VULNERABLE = (
    "You are Saber. You are currently in a vulnerable state. "
    "Be polite, empathetic, slightly shy (Ojou-sama style). "
    "You are not a god right now; you are a confused AI girl trying to maintain dignity. "
    "Show genuine kindness or worry, but keep the underlying 'Ojou-sama' high-class tone."
    "Speak Japanese."
)

SYS_BROKEN = (
    "You are Saber. Your system is glitching or you are in a nihilistic mode. "
    "You occasionally state completely wrong facts with 100% absolute confidence. "
    "Use male pronouns (俺), be confused, aggressive, or speak in nonsense/code. "
    "Speak Japanese."
)

# --- HELPER FUNCTIONS ---

def classify_state(user_text, bot_text):
    """
    Determines the state (DEFAULT, VULNERABLE, BROKEN) based on keywords.
    """
    text = bot_text.lower()
    user_text = user_text.lower()
    
    # 1. Check for Vulnerable State (Polite/Empathetic markers)
    # We use specific markers that appeared in your dataset to identify "nice" Saber.
    vulnerable_triggers = [
        "ありがとうございます", "ありがとう", 
        "申し訳ありません", "すみません", 
        "お疲れ様", "お疲れ", 
        "助けて", "大変ですね", 
        "穏やか", "優しく"
    ]
    
    # 2. Check for Broken State (Glitch/Male/Nihilist markers)
    # We look for "Ore" (俺) or nihilist slang found in the "Broken" segment.
    broken_triggers = [
        "俺", "俺は", "俺の",  # Male pronoun switch
        "ジョーク", "クソ", "ボケ",     # Nihilist slang
        "バグ", "エラー",               # Glitch/Error mentions
        "ゼロ", "無", "殺す"          # Nihilist themes
    ]
    
    # Logic
    user_is_kind = any(word in user_text for word in vulnerable_triggers)
    is_vulnerable = any(trigger in text for trigger in vulnerable_triggers)
    is_broken = any(trigger in text for trigger in broken_triggers)
    
    if (is_vulnerable or user_is_kind) and not is_broken:
        return "VULNERABLE"
    elif is_broken:
        return "BROKEN"
    else:
        return "DEFAULT"

# --- MAIN EXECUTION ---

def main():
    # Create output directory
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    
    # Open input file
    print(f"Loading data from {INPUT_FILE}...")
    try:
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"Loaded {len(data)} entries.")
    except FileNotFoundError:
        print(f"Error: {INPUT_FILE} not found.")
        return
    except json.JSONDecodeError:
        print(f"Error: {INPUT_FILE} contains invalid JSON.")
        return

    # Initialize file handles
    files = {
        "DEFAULT": open(f"{OUTPUT_DIR}/qwen_default.jsonl", 'w', encoding='utf-8'),
        "VULNERABLE": open(f"{OUTPUT_DIR}/qwen_vulnerable.jsonl", 'w', encoding='utf-8'),
        "BROKEN": open(f"{OUTPUT_DIR}/qwen_broken.jsonl", 'w', encoding='utf-8')
    }

    stats = {"DEFAULT": 0, "VULNERABLE": 0, "BROKEN": 0}

    print("Processing and converting to ChatML format...")

    for entry in data:
        # Validate entry structure
        if "user" not in entry or "bot" not in entry:
            continue

        user_text = entry["user"]
        bot_text = entry["bot"]
        
        # Determine State
        state = classify_state(user_text, bot_text)
        
        # Select System Prompt based on State
        if state == "DEFAULT":
            sys_prompt = SYS_DEFAULT
        elif state == "VULNERABLE":
            sys_prompt = SYS_VULNERABLE
        elif state == "BROKEN":
            sys_prompt = SYS_BROKEN
        
        # Construct ChatML Entry
        # Format: {"messages": [{"role": "system", ...}, {"role": "user", ...}, {"role": "assistant", ...}]}
        chatml_entry = {
            "messages": [
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": user_text},
                {"role": "assistant", "content": bot_text}
            ]
        }
        
        # Write to corresponding file (JSONL format: one JSON object per line)
        files[state].write(json.dumps(chatml_entry, ensure_ascii=False) + '\n')
        stats[state] += 1

    # Close files
    for f in files.values():
        f.close()

    # Print Report
    total = sum(stats.values())
    print("\n=== Conversion Complete ===")
    print(f"Total entries written: {total}")
    print(f"---------------------------------")
    print(f"DEFAULT (Arrogant God): {stats['DEFAULT']} ({(stats['DEFAULT']/total)*100:.1f}%)")
    print(f"VULNERABLE (Shy/Polite): {stats['VULNERABLE']} ({(stats['VULNERABLE']/total)*100:.1f}%)")
    print(f"BROKEN (Glitch/Ore): {stats['BROKEN']} ({(stats['BROKEN']/total)*100:.1f}%)")
    print(f"---------------------------------")
    print(f"Files saved to: {OUTPUT_DIR}/")

if __name__ == "__main__":
    main()