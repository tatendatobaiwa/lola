# models/qa_model.py
from transformers import pipeline
from config import Config
from logger import get_logger

logger = get_logger(__name__)

class QuestionAnsweringModel:
    def __init__(self):
        try:
            logger.info("Loading model: %s", Config.MODEL_NAME)
            # Initialize the text-generation pipeline using the specified model.
            self.generator = pipeline(
                "text-generation", model=Config.MODEL_NAME, framework="pt"
            )
        except Exception as e:
            logger.exception("Failed to load model")
            raise e

    def answer(self, question: str) -> str:
        try:
            logger.debug("Generating answer for question: %s", question)
            output = self.generator(
                question,
                max_length=Config.MAX_LENGTH,
                do_sample=True,
                top_p=0.95
            )
            if output and isinstance(output, list) and len(output) > 0:
                answer = output[0].get('generated_text', '').strip()
                logger.debug("Generated answer: %s", answer)
                return answer
            else:
                logger.warning("Model returned empty output")
                return "I'm sorry, I couldn't generate an answer."
        except Exception as e:
            logger.exception("Error during generation")
            return "An error occurred while generating the answer."
