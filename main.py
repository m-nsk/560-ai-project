import os
# from dotenv import load_dotenv
# from groq import Groq
from transcriber import GroqTranscriber #, LocalTranscriber


## Local whisper is much slower
# localTranscriber = LocalTranscriber()
# transcript = localTranscriber.transcribe("./test-files/trimmed.mp4")
# print(transcript)

groqTranscriber = GroqTranscriber()
filename = os.path.dirname(__file__) + "/test-files/trimmed.mp4"
transcript = groqTranscriber.transcribe(filename)
print(transcript)
