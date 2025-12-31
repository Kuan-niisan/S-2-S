import json
import numpy as np
import faiss
import MeCab
import sentencepiece as spm
from sentence_transformers import SentenceTransformer
import os
import torch

# ==========================================
# CONFIGURATION
# ==========================================
VECTOR_DATA_FILE = "data/vectorized/vectorized_data.json"
TOKENIZER_MODEL = "assets/tokenizer/sp_model.model"

class JapaneseChatBot:
    def __init__(self):
        print("Initializing Bot (CPU Mode)...")
        
        # 1. Load NLP Models with CPU
        
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.tagger = MeCab.Tagger()
        self.sp = spm.SentencePieceProcessor(model_file=TOKENIZER_MODEL)
        self.embedding_model = SentenceTransformer('sonoisa/sentence-bert-base-ja-mean-tokens-v2').to(device)
        
        # 2. Load Data
        print(f"Loading data from {VECTOR_DATA_FILE}...")
        with open(VECTOR_DATA_FILE, "r", encoding="utf-8") as f:
            self.dataset = json.load(f)
            
        # 3. Prepare Matrix
        vectors = np.array([item["input_vector"] for item in self.dataset]).astype('float32')
        
        # 4. Build FAISS Index (CPU Only)
        # IndexFlatL2 is the standard CPU implementation for Exact Search
        dimension = vectors.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        
        self.index.add(vectors)
        print("✓ FAISS Index built on CPU.")
        print("✓ Index Ready.")

    def preprocess(self, text):
        """MeCab Lemmatization"""
        node = self.tagger.parseToNode(text)
        lemmas = []
        while node:
            if node.surface != "":
                features = node.feature.split(',')
                # Filter Particles/Symbols
                if features[0] not in ["助詞", "補助記号"]:
                    lemma = features[6] if len(features) > 6 else node.surface
                    if lemma == '*': lemma = node.surface
                    lemmas.append(lemma)
            node = node.next
        
        # Return lemmatized string
        return " ".join(lemmas)

    def get_response(self, user_text):
        # 1. Preprocess & Vectorize
        clean_text = self.preprocess(user_text)
        
        # 2. Embedding
        vec = self.embedding_model.encode(clean_text).astype('float32').reshape(1, -1)
        
        # 3. Search
        k = 1 # Get top 1 result
        distances, indices = self.index.search(vec, k)
        
        # 4. Retrieve Response
        best_idx = indices[0][0]
        return self.dataset[best_idx]["raw_response"]

def main():
    bot = JapaneseChatBot()
    
    print("\n--- CHATBOT STARTED (CPU) ---")
    print("Type 'quit' to exit.")
    
    while True:
        try:
            user_input = input("User: ")
            if user_input.lower() == 'quit':
                break
            
            reply = bot.get_response(user_input)
            print(f"Bot: {reply}")
            
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()