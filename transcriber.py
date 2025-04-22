"""Transcribe using Whisper or Groq"""

import whisper
from dotenv import load_dotenv
from groq import Groq

import subprocess
import tempfile
import os

class LocalTranscriber:
    """Runs whisper from command line instead of Python bindings for Windows compatibility."""
    def __init__(self, model_name="base"):
        self.model_name = model_name

    def transcribe(self, file_path: str) -> str:
        with tempfile.TemporaryDirectory() as tmpdir:
            command = [
                "whisper",
                file_path,
                "--model", self.model_name,
                "--output_format", "txt",
                "--output_dir", tmpdir
            ]
            subprocess.run(command, check=True)

            base_filename = os.path.splitext(os.path.basename(file_path))[0]
            output_file = os.path.join(tmpdir, f"{base_filename}.txt")

            with open(output_file, "r", encoding="utf-8") as f:
                return f.read()


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
