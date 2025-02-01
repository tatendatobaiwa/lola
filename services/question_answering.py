# services/question_answering.py
from models.qa_model import QuestionAnsweringModel
from logger import get_logger

logger = get_logger(__name__)

class QuestionAnsweringService:
    def __init__(self):
        self.qa_model = QuestionAnsweringModel()

    def get_answer(self, question: str) -> str:
        if not question or not question.strip():
            logger.warning("Received empty question")
            return "Please provide a valid question."
        return self.qa_model.answer(question)
