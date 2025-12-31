import os
import json
from src.config import DATA_DIR, PROCESSED_DATA_PATH

def prepare_dataset():
    """
    Reads data from the /data directory and converts it into 
    the JSONL format required for Qwen finetuning.
    """
    print("Preparing dataset for finetuning...")
    
    # Placeholder logic - needs to be adapted to the specific format of files in /data
    # e.g., reading corpus.txt or data_generated.json
    
    # Output format example:
    # {"messages": [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]}
    
    data = []
    
    # TODO: Implement logic to read from DATA_DIR
    
    print(f"Dataset prepared. Saving to {PROCESSED_DATA_PATH}...")
    # with open(PROCESSED_DATA_PATH, 'w', encoding='utf-8') as f:
    #     for item in data:
    #         f.write(json.dumps(item, ensure_ascii=False) + '\n')

if __name__ == "__main__":
    prepare_dataset()
