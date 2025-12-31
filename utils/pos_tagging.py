import json
import MeCab
import collections
import os
import unidic

# Load cleaned data
parent_dir = os.path.dirname(os.path.abspath(__file__))
cleaned_data_path = os.path.join(parent_dir, '..', 'cleaned_data.json')
with open(cleaned_data_path, 'r', encoding='utf-8') as f:
    dataset = json.load(f)

# Init tagger
tagger = MeCab.Tagger('-d "{}"'.format(unidic.DICDIR))

# POS Tagging
def get_pos_features(text):
    """
    Parses text to extract POS Tags (HMM Emission).
    Returns the list of (Lemma, POS) tuples.
    """
    node = tagger.parseToNode(text)
    pos_features = []
    
    while node:
        if node.surface != '':
            features = node.feature.split(',')
            surface = node.surface
            pos = features[0]
            lemma = features[6] if len(features) > 6 else surface
            
            # Clean up lemma
            if lemma == '*' or lemma == '':
                lemma = surface
            
            pos_main = features[0]      # e.g., 名詞, 動詞
            pos_sub = features[1]       # e.g., 一般, 固有名詞
            
            pos_features.append({
                "lemma": lemma,
                "pos": pos_main,
                "sub_pos": pos_sub
            })
        node = node.next
    return pos_features

# ==========================================
# AMBIGUITY DETECTION (The "HMM" Logic)
# ==========================================

# In a real HMM, we calculate probabilities. 
# Here, we simulate disambiguation by flagging words that appear 
# with generic tags versus specific tags.

def add_disambiguation_flags(dataset):
    """
    Adds a 'disambiguation' field to the dataset.
    Helps the NN focus on Ambiguous Nouns.
    """
    updated_data = []
    
    # Simple frequency dictionary (Simulating Probabilities)
    # In a real app, this would be a massive corpus count
    lemma_counts = collections.Counter()
    
    # First pass: build lemma to POS tag mapping
    for entry in dataset:
        # Re-parse the original raw text to get full POS info (including particles)
        # We use raw_input because lemmatized_input lost particles
        features = get_pos_features(entry["raw_input"])
        
        # Count lemma frequencies for this dataset
        for f in features:
            lemma_counts[f["lemma"]] += 1
            
        # Identify "Generic Nouns" (Potential Ambiguity)
        # If a lemma is tagged '一般' (General) Noun, it might be ambiguous
        # If it is '固有' (Proper), it is specific (less ambiguous)
        is_ambiguous = any(f["pos"] == "名詞" and f["sub_pos"] == "一般" for f in features)
        
        entry["is_generic_sentence"] = is_ambiguous
        entry["pos_sequence"] = features # Store the HMM emission sequence
        updated_data.append(entry)
    
    return updated_data, lemma_counts

enhanced_dataset, lemma_frequencies = add_disambiguation_flags(dataset)

output_file = os.path.join(parent_dir, '..', 'pos_labeled_data.json')
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(enhanced_dataset, f, ensure_ascii=False, indent=2)
    
print(f"✓ Step 3 Complete: POS Disambiguation added to {output_file}")

# --- ANALYSIS OF THE RESULT ---
print("\n--- POS ANALYSIS ---")
print("Lemma Frequencies in Dataset (HMM State Observations):")
# Show top 3 most frequent words
for lemma, count in lemma_frequencies.most_common(3):
    print(f"  - {lemma}: {count} times")

# Show how the POS data looks for one entry
sample = enhanced_dataset[0]
print(f"\nSample Sentence: {sample['raw_input']}")
print("POS Sequence (HMM Emissions):")
for token in sample["pos_sequence"][:3]: # Show first 3 tokens
    print(f"  - Surface: {token['lemma']}, POS: {token['pos']}")

if sample["is_generic_sentence"]:
    print(">> Status: Contains Generic Nouns (Potential Ambiguity)")
else:
    print(">> Status: Context Specific")