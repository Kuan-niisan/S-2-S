from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments
from peft import LoraConfig, get_peft_model
# from trl import SFTTrainer # Common choice for instruction tuning
from src.config import BASE_MODEL_PATH, ADAPTER_PATH, PROCESSED_DATA_PATH

def train():
    print(f"Starting training for {BASE_MODEL_PATH}...")
    
    # 1. Load Model & Tokenizer
    # 2. Load Dataset (PROCESSED_DATA_PATH)
    # 3. Configure LoRA
    # 4. Initialize Trainer
    # 5. Train
    # 6. Save Adapter to ADAPTER_PATH
    
    pass

if __name__ == "__main__":
    train()
