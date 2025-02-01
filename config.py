# config.py
import os

class Config:
    # Switch to a CPU-friendly smaller model
    MODEL_NAME = os.getenv("MODEL_NAME", "deepseek-ai/deepseek-llm-7b-chat")  # Smaller variant
    MAX_LENGTH = int(os.getenv("MAX_LENGTH", "128")) 
    VOICE_RATE = int(os.getenv("VOICE_RATE", "150"))
    VOICE_VOLUME = float(os.getenv("VOICE_VOLUME", "1.0"))
    DEVICE = "cpu"  
    TORCH_DTYPE = "float32"  