import os
from dotenv import load_dotenv
from transcriber import GroqTranscriber, LocalTranscriber
from llm_processor import GroqProcessor
from groq import Groq
import pymupdf4llm
import json
from flashcards_maker import generate_anki_deck

load_dotenv()

# Establish single Groq client instance
groq_client = Groq()

transcript = None

# groqTranscriber = GroqTranscriber(groq_client)
# localTranscriber = LocalTranscriber()
# filename = os.path.dirname(__file__) + "/test-files/550 8.1 8.2 compressed.mp3"
# transcript = groqTranscriber.transcribe(filename)
# transcript = localTranscriber.transcribe(filename)
# print(transcript)

with open("test-files/550 8.1 8.2 transcript.txt", "r") as f:
    transcript = f.read() # TODO: the transcript is being fed manually just so we don't have to call Whisper every time. The above whisper code works!

slides = None
# Process PDF slides using pymupdf4llm
slides = pymupdf4llm.to_markdown("./test-files/550 8.1 8.2.pdf")
with open("./test-files/slides_markdown.md", "w", encoding="utf-8") as f:
    f.write(slides)

llm_processor = GroqProcessor(groq_client)
result = llm_processor.process_transcript(transcript=transcript, slides=slides) # TODO: LLM request can fail randomly because of json validation

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

# Generate Anki deck from response
topic_name = "550-8.1-8.2"
generate_anki_deck(result["flashcards"], topic_name)