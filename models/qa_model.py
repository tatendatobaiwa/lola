# models/qa_model.py
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from config import Config
from logger import get_logger

logger = get_logger(__name__)

class QuestionAnsweringModel:
    def __init__(self):
        try:
            logger.info("Loading CPU-optimized model: %s", Config.MODEL_NAME)
            
            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(
                Config.MODEL_NAME,
                trust_remote_code=True
            )

            # Load model with CPU optimizations
            self.model = AutoModelForCausalLM.from_pretrained(
                Config.MODEL_NAME,
                trust_remote_code=True,
                device_map=Config.DEVICE,
                torch_dtype=getattr(torch, Config.TORCH_DTYPE),
                low_cpu_mem_usage=True  # Critical for CPU
            )
            
            # Create pipeline for easier CPU usage
            self.pipeline = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                device=-1  # Force CPU
            )
            
            logger.info("CPU model loaded successfully")

        except Exception as e:
            logger.exception("CPU model loading failed")
            raise RuntimeError(f"CPU load error: {str(e)}") from e

    def answer(self, question: str) -> str:
        try:
            # Generate with CPU-friendly parameters
            outputs = self.pipeline(
                question,
                max_new_tokens=Config.MAX_LENGTH,
                do_sample=True,
                top_p=0.9,
                temperature=0.7,
                pad_token_id=self.tokenizer.eos_token_id
            )
            
            return outputs[0]['generated_text'].strip()
            
        except Exception as e:
            logger.exception("CPU generation error")
            return "Error generating answer (CPU)"

    def answer(self, question: str) -> str:
        try:
            inputs = self.tokenizer(
                question,
                return_tensors="pt",
                padding=True,
                truncation=True
            ).to(self.model.device)

            outputs = self.model.generate(
                **inputs,
                max_new_tokens=Config.MAX_LENGTH,
                do_sample=True,
                top_p=0.95,
                temperature=0.8
            )
            
            return self.tokenizer.decode(
                outputs[0],
                skip_special_tokens=True
            ).strip()
            
        except Exception as e:
            logger.exception("Generation error")
            return "Error generating answer"