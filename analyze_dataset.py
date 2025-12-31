import json
import collections

def analyze_dataset(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    total = len(data)
    categories = collections.Counter()
    
    # Define keywords for detection
    # "Therapist" patterns (Polite, helpful, philosophical)
    therapist_keywords = ["意味", "心", "穏やか", "人生", "悩み", "大切", "お疲れ", "申し訳", "癒や", "希望", "支え", "成長", "共感"]
    
    # "Gamer" patterns (Specific slang, specific context)
    gamer_keywords = ["ガチャ", "課金", "運", "ゲーム", "ログイン", "クエスト", "リセマラ", "すり抜け", "爆死", "運営", "天井"]
    
    # "Narcissist" patterns (Arrogant, Self-centered, Insulting)
    narcissist_keywords = ["愚か", "凡俗", "完璧", "美学", "光栄", "私", "貴様", "雑種", "ひれ伏", "絶望", "Saber"]

    for entry in data:
        text = entry['bot']
        
        # Simple keyword matching (Priority: Gamer > Therapist > Narcissist > Neutral)
        # Gamer terms are very specific
        if any(k in text for k in gamer_keywords):
            categories['Toxic Gamer'] += 1
            continue
            
        # Therapist terms are distinct from Narcissist
        if any(k in text for k in therapist_keywords):
            categories['Therapist/Polite'] += 1
            continue
            
        # Narcissist terms
        if any(k in text for k in narcissist_keywords):
            categories['Narcissist'] += 1
            continue
            
        categories['Uncategorized/Neutral'] += 1

    print(f"Total Entries: {total}")
    print("\n--- Personality Distribution ---")
    for cat, count in categories.most_common():
        percentage = (count / total) * 100
        print(f"{cat}: {count} ({percentage:.1f}%)")

if __name__ == "__main__":
    analyze_dataset('data/data_generated_processed.json')
