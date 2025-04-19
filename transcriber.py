"""Transcribe using Whisper or Groq"""

import whisper
from dotenv import load_dotenv
from groq import Groq

class LocalTranscriber:
    """Whisper wrapper"""
    def __init__(self, model_name: str = "base"):
        self.model = whisper.load_model(model_name)

    def transcribe(self, file_path: str) -> str:
        result = self.model.transcribe(file_path, fp16=False)
        return result["text"]

class GroqTranscriber:
    """Groq API wrapper for transcription"""
    def __init__(self, client: Groq, model_name: str = "whisper-large-v3"):
        self.client = client
        self.model_name = model_name

    def transcribe(self, file_path: str) -> str:
        """Transcribe audio file using Groq API"""
        with open(file_path, "rb") as file:
            transcription = self.client.audio.transcriptions.create(
                file=(file_path, file.read()),
                model=self.model_name,
                response_format="verbose_json",
            )
            return transcription.text
