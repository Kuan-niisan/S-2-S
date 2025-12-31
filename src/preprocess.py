import json
import MeCab
import collections
import os

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "data", "processed")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "pos_labeled_data.json")
DATA_DIR = os.path.join(BASE_DIR, "data")
DATA_FILE = os.path.join(DATA_DIR, "data_generated_processed.json")

# Get real data function
def get_data():
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def process_with_unidic(data_pairs):
    processed_data = []
    tagger = MeCab.Tagger()
    unknown_words = set()
    
    def parse_text(text):
        node = tagger.parseToNode(text)
        tokens = []
        lemmas = []
        while node:
            if node.surface != "":
                features = node.feature.split(',')
                surface = node.surface
                pos = features[0]
                lemma = features[6] if len(features) > 6 else surface
                if lemma == '*': lemma = surface
                
                if pos == "未知語": unknown_words.add(surface)

                # Filter Particles (Clean Data Step)
                if pos not in ["助詞", "補助記号"]:
                    tokens.append({"surface": surface, "lemma": lemma, "pos": pos})
                    lemmas.append(lemma)
            node = node.next
        return tokens, " ".join(lemmas)

    for pair in data_pairs:
        u_tokens, u_lemmas = parse_text(pair["user"])
        
        # HMM Disambiguation Logic (Basic)
        is_generic = any(t["pos"] == "名詞" for t in u_tokens)

        entry = {
            "raw_input": pair["user"],
            "raw_response": pair["bot"],
            "lemmatized_input": u_lemmas,
            "tokens": u_tokens,
            "is_generic_sentence": is_generic
        }
        processed_data.append(entry)

    return processed_data, unknown_words

if __name__ == "__main__":
    # Create directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    raw_data = get_data()
    final_data, unknowns = process_with_unidic(raw_data)
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(final_data, f, ensure_ascii=False, indent=4)
    
    print(f"✓ Preprocessing complete. Saved to {OUTPUT_FILE}")