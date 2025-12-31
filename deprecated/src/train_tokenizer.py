import json
import sentencepiece as spm
import os

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_FILE = os.path.join(BASE_DIR, "data/processed/pos_labeled_data.json")
CORPUS_FILE = os.path.join(BASE_DIR, "data/corpus.txt")
TOKENIZER_DIR = os.path.join(BASE_DIR, "assets/tokenizer")
MODEL_PREFIX = os.path.join(TOKENIZER_DIR, "sp_model")

def main():
    # Create tokenizer directory
    os.makedirs(TOKENIZER_DIR, exist_ok=True)
    
    # 1. Load Data
    print("Loading lemmas...")
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        dataset = json.load(f)

    # 2. Create Corpus for BPE
    print("Creating corpus...")
    with open(CORPUS_FILE, "w", encoding="utf-8") as f:
        for entry in dataset:
            f.write(entry["lemmatized_input"] + "\n")

    # 3. Train SentencePiece
    print("Training SentencePiece (BPE)...")
    spm.SentencePieceTrainer.train(
        input=CORPUS_FILE,
        model_prefix=MODEL_PREFIX,
        vocab_size=115,
        model_type='bpe',
        character_coverage=0.995,
        user_defined_symbols=['<pad>', '<start>', '<end>']
    )
    
    print(f"✓ Tokenizer trained and saved to {TOKENIZER_DIR}")

if __name__ == "__main__":
    main()