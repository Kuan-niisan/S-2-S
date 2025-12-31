import json
import numpy as np
from sentence_transformers import SentenceTransformer
import os
import torch

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_FILE = os.path.join(BASE_DIR, "data/processed/pos_labeled_data.json")
OUTPUT_DIR = os.path.join(BASE_DIR, "data/vectorized")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "vectorized_data.json")

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 1. Load Data
    print("Loading processed data...")
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        dataset = json.load(f)

    # 2. Load SBERT Model
    print("Loading SBERT model (v2)...")
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model = SentenceTransformer('sonoisa/sentence-bert-base-ja-mean-tokens-v2').to(device)

    # 3. Vectorize
    print("Vectorizing...")
    for entry in dataset:
        text = entry["lemmatized_input"]
        vector = model.encode(text)
        entry["input_vector"] = vector.tolist()
    
    print(f"✓ Vectorization complete. {len(dataset)} entries processed.")

    # 4. Save
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)
        
    print(f"✓ Vectors saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()