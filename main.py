import os
from dotenv import load_dotenv
from transcriber import GroqTranscriber
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

# Primitive fix to LLm request failing randomly -> Continues trying until valid response
counter = 0
while True:
    counter += 1
    try:
        result = llm_processor.process_transcript(transcript=transcript, slides=slides)
        print(f"LLM request made successfully after {counter:02d} attempts.")
        counter = 0
        break
    except Exception:
        continue

#result = llm_processor.process_transcript(transcript=transcript, slides=slides) # TODO: LLM request can fail randomly because of json validation
topic_name = "550"

# TODO: parse these into actual files instead of just debug output




preamble = r"""\documentclass[11pt]{article}
\usepackage[utf8]{inputenc}
\usepackage{amsmath, amssymb}
\usepackage{enumitem}
\usepackage{graphicx}
\usepackage{geometry}
\usepackage{hyperref}
\usepackage{xcolor}

\geometry{margin=1in}
"""


print("\n=== Notes ===")
print(result["notes"])

print("\n=== Quiz Questions ===")
print(result["quiz"])


def wrap_latex(preamble: str, document: str) -> str:
    return f"{preamble}\n{document}"

# Write lecture notes
with open(f"./generated-files/{topic_name}_notes.tex", "w", encoding="utf-8") as f:
    f.write(wrap_latex(preamble, result["notes"]))

# Write quiz
with open(f"./generated-files/{topic_name}_quiz.tex", "w", encoding="utf-8") as f:
    f.write(wrap_latex(preamble, result["quiz"]))


# Generate Anki deck from response
generate_anki_deck(result["flashcards"], topic_name)
