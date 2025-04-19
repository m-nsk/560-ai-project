import os
from dotenv import load_dotenv
from transcriber import GroqTranscriber #, LocalTranscriber
from llm_processor import GroqProcessor

load_dotenv()

## Local whisper is much slower
# localTranscriber = LocalTranscriber()
# transcript = localTranscriber.transcribe("./test-files/trimmed.mp4")
# print(transcript)

groqTranscriber = GroqTranscriber()
filename = os.path.dirname(__file__) + "/test-files/trimmed.mp4"
transcript = groqTranscriber.transcribe(filename)
print(transcript)

llm_processor = GroqProcessor()
llm_processor.process_transcript(transcript)
