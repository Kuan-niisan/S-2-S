2. The Execution Flow (Order of Files)
You must run the files in this specific order to build the pipeline. Do this from your NLP_Project root folder.

Step 1: Data Preparation
Command: python src/preprocess.py
Action: Reads raw data, cleans it using MeCab, performs HMM disambiguation analysis.
Output: data/processed/pos_labeled_data.json

Step 2: Train Tokenizer
Command: python src/train_tokenizer.py
Action: Reads the clean lemmas from Step 1, trains the SentencePiece model.
Output: assets/tokenizer/sp_model.model + data/corpus.txt

Step 3: Create Vectors (Feature Extraction)
Command: python src/embedding.py
Action: Loads the data from Step 1, converts the text into 768-dimension vectors.
Output: data/vectorized/vectorized_data.json

Step 4: Run the Bot
Command: python main.py
Action: Loads the Vectors from Step 3 and the Model from Step 2. Initializes FAISS and starts the chat loop.