import MeCab
import json
import os
import unidic

# Init tagger
try:
    tagger = MeCab.Tagger('-d "{}"'.format(unidic.DICDIR))
except RuntimeError as e:
    print(f"ERROR: Could not initialize MeCab with path: {unidic.DICDIR}")
    print(f"Please verify the path exists on your Windows machine.")
    print(f"Details: {e}")
    exit()
    
def unidic_process(data_pairs):
    processed_data = []
    unknown_words = set()
    
    for pair in data_pairs:
        user_text = pair['user']
        bot_text = pair['bot']
        
        # Process user text
        def parse_text(text):
            node = tagger.parseToNode(text)
            tokens = []
            lemmas = []
            
            while node:
                if node.surface != '':
                    
                    # --- UNIDIC FEATURE MAPPING ---
                    # UniDic feature structure (simplified):
                    # 0: POS, 1: SubPOS, 2: SubPOS2, 3: SubPOS3, 
                    # 4: Type, 5: Form, 
                    # 6: LEMMA (The Root Form) <--- This is our target!
                    # 7: Orthography...
                    
                    features = node.feature.split(',')
                    surface = node.surface
                    pos = features[0]
                    #Extract lemma
                    lemma = features[6] if len(features) > 6 else surface
                    
                    # Clean up lemma
                    if lemma == '*' or lemma == '':
                        lemma = surface
                    
                    #Check for unknown words
                    if pos == '未知語':
                        unknown_words.add(surface)
                    
                    token_data = {
                        'surface': surface,
                        'lemma': lemma,
                        'pos': pos
                    }
                    tokens.append(token_data)
                    lemmas.append(lemma)
            
                node = node.next
            
            return tokens, " ".join(lemmas)

        # Process user and bot texts and lemmas
        user_tokens, user_lemmas = parse_text(user_text)
        bot_tokens, bot_lemmas = parse_text(bot_text)
        
        entry = {
            "raw_input": user_text,
            "raw_response": bot_text,
            "lemmatized_input": user_lemmas, # Feed this to your NN
            "lemmatized_response": bot_lemmas,
            "unidic_tokens": user_tokens
        }
        
        processed_data.append(entry)
    
    return processed_data, unknown_words


# INPUT MOCK CONVERSATION DATA
raw_data = [
    {
        "user": "今日はとても疲れたから早く寝たい",
        "bot": "ゆっくり休んでね。明日も頑張ろう！"
    },
    {
        "user": "この映画は面白かったけど、少し悲しかった",
        "bot": "感動的なシーンが多かったんだね"
    },
    {
        "user": "新しいゲームを買ってきた",
        "bot": "何を買ったの？一緒に遊ぼう"
    }
]

# GET DATA FROM DISCORD MESSAGES WITH THE MODEL



# PROCESS DATA
print("Processing data with UniDic...")
processed_data, unknown_words = unidic_process(raw_data)

#SAVE PROCESSED DATA to raw_data.json
output_path = "raw_data.json"
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(processed_data, f, ensure_ascii=False, indent=4)
print(f"Processed data saved to {output_path}")

#Output Analysis
print("\n--- SAMPLE ENTRY ---")
print(f"Raw: {processed_data[0]['raw_input']}")
print(f"Lemmatized (Input to NN): {processed_data[0]['lemmatized_input']}")

print("\n--- UNIDIC VERIFICATION ---")

check_verb = processed_data[0]['unidic_tokens']
for token in check_verb:
    if token['surface'] == '疲れた':
        print(f"✓ Stemming Success: '{token['surface']}' (tired) -> '{token['lemma']}' (to get tired)")
        break

if unknown_words:
    print("\n--- UNKNOWN WORDS DETECTED ---")
    for word in unknown_words:
        print(f"Unknown word: {word}")
        


