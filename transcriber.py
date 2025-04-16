"""Transcribe using Whisper"""

import whisper

class Transcriber:
    """Whisper wrapper"""
    def __init__(self, model_name: str = "base"):
        self.model = whisper.load_model(model_name)

    def transcribe(self, file_path: str) -> str:
        result = self.model.transcribe(file_path)
        return result["text"]


model = whisper.load_model("base")
result = model.transcribe("./test-files/trimmed.mp4")

print(result)
