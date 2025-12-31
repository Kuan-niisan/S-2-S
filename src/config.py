import os
from dotenv import load_dotenv

load_dotenv()

# Discord Configuration
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
COMMAND_PREFIX = os.getenv("COMMAND_PREFIX", "!")

# Model Configuration
# User specified model ID
MODEL_ID = "qwen3:1.7b" 
# Fallback/Base model for technical implementation if specific ID isn't on HF yet
BASE_MODEL_PATH = os.getenv("BASE_MODEL_PATH", "Qwen/Qwen2.5-1.5B-Instruct")

# Paths
ADAPTER_PATH = os.path.join("models", "qwen_finetuned_adapter")
DATA_DIR = os.path.join("data")
PROCESSED_DATA_PATH = os.path.join("data", "processed", "finetune_dataset.jsonl")

# Training Configuration
MAX_LENGTH = 512
BATCH_SIZE = 4
GRADIENT_ACCUMULATION_STEPS = 4
LEARNING_RATE = 2e-4
EPOCHS = 3
