# models/qa_model.py

from transformers import AutoTokenizer, AutoModelForCausalLM
from config import Config
from logger import get_logger

logger = get_logger(__name__)

class QuestionAnsweringModel:
    def __init__(self):
        try:
            logger.info("Loading model: %s", Config.MODEL_NAME)
            # Load the tokenizer and model directly using the provided identifier.
            self.tokenizer = AutoTokenizer.from_pretrained(
                Config.MODEL_NAME, 
                trust_remote_code=True
            )
            self.model = AutoModelForCausalLM.from_pretrained(
                Config.MODEL_NAME, 
                trust_remote_code=True
            )
            logger.info("Model loaded successfully")
        except Exception as e:
            logger.exception("Failed to load model")
            raise e

    def answer(self, question: str) -> str:
        try:
            logger.debug("Generating answer for question: %s", question)
            # Tokenize the input question.
            input_ids = self.tokenizer.encode(question, return_tensors="pt")
            
            # Generate output using the model.
            output_ids = self.model.generate(
                input_ids,
                max_length=Config.MAX_LENGTH,
                do_sample=True,
                top_p=0.95
            )
            
            # Decode the output tokens to get the answer.
            answer = self.tokenizer.decode(output_ids[0], skip_special_tokens=True).strip()
            logger.debug("Generated answer: %s", answer)
            return answer
        except Exception as e:
            logger.exception("Error during answer generation")
            return "An error occurred while generating the answer."
