import sys
import os

# ==========================================
# 1. CONFIGURE PATHS
# ==========================================

# Get the directory of this script (the root folder)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Define the source directory
src_dir = os.path.join(current_dir, 'src')

# Add 'src' to Python's system path
if src_dir not in sys.path:
    sys.path.append(src_dir)

# ==========================================
# 2. IMPORT AND RUN BOT
# ==========================================

# Now we can import 'bot' directly because we added src to path
import bot

if __name__ == "__main__":
    # Call the 'main' function defined inside bot.py
    bot.main()