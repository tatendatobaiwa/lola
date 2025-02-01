# config.py

import os

class Config:
    # Update the model name to use the direct identifier.
    MODEL_NAME = os.getenv("MODEL_NAME", "deepseek-ai/DeepSeek-R1")
    MAX_LENGTH = int(os.getenv("MAX_LENGTH", "150"))
    VOICE_RATE = int(os.getenv("VOICE_RATE", "150"))
    VOICE_VOLUME = float(os.getenv("VOICE_VOLUME", "1.0"))
    # Optionally, include a Hugging Face token if needed:
    HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN", "")
