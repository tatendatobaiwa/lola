# config.py
import os

class Config:
    # The Hugging Face model to use (DeepSeek R1 in this case).
    MODEL_NAME = os.getenv("MODEL_NAME", "deepseek/R1")
    
    # Maximum length of generated text.
    MAX_LENGTH = int(os.getenv("MAX_LENGTH", "150"))
    
    # Text-to-Speech (TTS) parameters (if needed).
    VOICE_RATE = int(os.getenv("VOICE_RATE", "150"))
    VOICE_VOLUME = float(os.getenv("VOICE_VOLUME", "1.0"))
