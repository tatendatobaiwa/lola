# services/voice_service.py
import io
import pyttsx3
from config import Config
from logger import get_logger

logger = get_logger(__name__)

class VoiceService:
    def __init__(self):
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', Config.VOICE_RATE)
            self.engine.setProperty('volume', Config.VOICE_VOLUME)
            logger.info("Initialized TTS engine successfully")
        except Exception as e:
            logger.exception("Failed to initialize TTS engine")
            raise e

    def text_to_speech(self, text: str) -> bytes:
        """
        Convert text to speech and return the audio as binary data (WAV format).
        """
        try:
            # pyttsx3 doesn't natively support returning audio as binary,
            # so we use a temporary file workaround.
            import tempfile
            temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
            temp_file_name = temp_file.name
            temp_file.close()

            # Save the synthesized speech to the temporary file.
            self.engine.save_to_file(text, temp_file_name)
            self.engine.runAndWait()

            # Read the audio data from the file.
            with open(temp_file_name, "rb") as f:
                audio_data = f.read()
            logger.debug("Generated audio for text")
            return audio_data
        except Exception as e:
            logger.exception("Error during TTS conversion")
            raise e
