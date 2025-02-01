# main.py
from fastapi import FastAPI, HTTPException, Response
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from services.question_answering import QuestionAnsweringService
from services.voice_service import VoiceService
from logger import get_logger

app = FastAPI(
    title="Lola - Offline AI Assistant",
    version="1.0",
    description="A production-ready offline Q&A and voice assistant powered by DeepSeek R1."
)
logger = get_logger(__name__)

# Allow CORS for local testing (adjust in production).
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for the frontend.
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize our services.
qa_service = QuestionAnsweringService()
voice_service = VoiceService()

# Request and Response models.
class QuestionRequest(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    answer: str

@app.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):
    try:
        answer = qa_service.get_answer(request.question)
        return AnswerResponse(answer=answer)
    except Exception as e:
        logger.exception("Error processing question")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/ask_voice")
async def ask_question_voice(request: QuestionRequest):
    try:
        answer = qa_service.get_answer(request.question)
        audio_data = voice_service.text_to_speech(answer)
        return Response(content=audio_data, media_type="audio/wav")
    except Exception as e:
        logger.exception("Error processing voice response")
        raise HTTPException(status_code=500, detail="Internal server error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
