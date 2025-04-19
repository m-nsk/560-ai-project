import os
from dotenv import load_dotenv
from transcriber import GroqTranscriber #, LocalTranscriber
from llm_processor import GroqProcessor
from groq import Groq
import json

load_dotenv()

# Create a single Groq client instance
groq_client = Groq()

## Local whisper is much slower
# localTranscriber = LocalTranscriber()
# transcript = localTranscriber.transcribe("./test-files/trimmed.mp4")
# print(transcript)

# groqTranscriber = GroqTranscriber(groq_client)
# filename = os.path.dirname(__file__) + "/test-files/trimmed.mp4"
# transcript = groqTranscriber.transcribe(filename)

with open("test-files/generated_transcript.txt", "r") as f:
    transcript = f.read() # TODO: the transcript is being fed manually just so we don't have to call Whisper every time. The above whisper code works!

slides = None # TODO: add PDF to plaintext conversion

llm_processor = GroqProcessor(groq_client)
result = llm_processor.process_transcript(transcript=transcript, slides=slides)

# TODO: parse these into actual files instead of just debug output
print("\n=== Notes ===")
for note in result["notes"]:
    print(f"\nTitle: {note['title']}")
    print("Content:")
    print(note['content'])

print("\n=== Quiz Questions ===")
for i, question in enumerate(result["quiz"], 1):
    print(f"\nQuestion {i}: {question['question']}")
    print("Options:")
    for option in question['options']:
        print(f"- {option}")
    print(f"Correct Answer: {question['correct_answer']}")

print("\n=== Flashcards ===")
for i, card in enumerate(result["flashcards"], 1):
    print(f"\nCard {i}:")
    print(f"Front: {card['front']}")
    print(f"Back: {card['back']}")
