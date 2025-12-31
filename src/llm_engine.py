import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
from .config import BASE_MODEL_PATH, ADAPTER_PATH, MODEL_ID
import os

class LLMEngine:
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

    def load_model(self):
        """
        Loads the Qwen model. 
        If an adapter exists in 'models/', it loads the Finetuned version.
        Otherwise, it loads the base model.
        """
        print(f"Loading Base Model: {BASE_MODEL_PATH} ({MODEL_ID})...")
        
        # Load Tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL_PATH, trust_remote_code=True)
        
        # Load Base Model
        # Note: In a real scenario with 1.7B, we might use 4bit/8bit loading for efficiency
        self.model = AutoModelForCausalLM.from_pretrained(
            BASE_MODEL_PATH,
            device_map="auto",
            trust_remote_code=True,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
        )

        # Check for Finetuned Adapter
        if os.path.exists(ADAPTER_PATH):
            print(f"Found adapter at {ADAPTER_PATH}. Loading PEFT model...")
            self.model = PeftModel.from_pretrained(self.model, ADAPTER_PATH)
        
        self.model.eval()

    def generate_response(self, user_input, user_name="User"):
        if not self.model:
            return "Error: Model not loaded."

        # Construct Prompt (Chat Template)
        # Adjust specific template for Qwen
        messages = [
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": user_input}
        ]
        
        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        
        model_inputs = self.tokenizer([text], return_tensors="pt").to(self.device)

        generated_ids = self.model.generate(
            model_inputs.input_ids,
            max_new_tokens=512
        )
        
        generated_ids = [
            output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]

        response = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        return response
