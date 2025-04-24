import os
from dotenv import load_dotenv
from transcriber import GroqTranscriber
from llm_processor import GroqProcessor
from groq import Groq
import pymupdf4llm
import json
from flashcards_maker import generate_anki_deck
from pdf_to_latex import compile_tex_to_pdf

load_dotenv()

# Establish single Groq client instance
groq_client = Groq()
llm_processor = GroqProcessor(groq_client)

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

def wrap_latex(preamble: str, document: str) -> str:
    return f"{preamble}\n{document}"

def process(pdf_path, audio_path, topic_name):

    transcript = None

    # groqTranscriber = GroqTranscriber(groq_client)
    # localTranscriber = LocalTranscriber()
    # filename = os.path.dirname(__file__) + "/test-files/550 8.1 8.2 compressed.mp3"
    # transcript = groqTranscriber.transcribe(filename)
    # transcript = localTranscriber.transcribe(filename)
    # print(transcript)

    with open(f"demo-files/{audio_path[:len(audio_path-3)]}txt", "r") as f:
        transcript = f.read() # TODO: the transcript is being fed manually just so we don't have to call Whisper every time. The above whisper code works!

    slides = None
    # Process PDF slides using pymupdf4llm
    slides = pymupdf4llm.to_markdown(f"./demo-files/{pdf_path}")
    # with open("./test-files/slides_markdown.md", "w", encoding="utf-8") as f:
    #     f.write(slides)

    # Primitive fix to LLm request failing randomly -> Continues trying until valid response
    counter = 0
    while True:
        counter += 1
        try:
            result = llm_processor.process_transcript(transcript=transcript, slides=slides)
            print(f"LLM request made successfully after {counter} attempts.")
            counter = 0
            break
        except Exception:
            continue

    # print("\n=== Notes ===")
    # print(result["notes"])

    # print("\n=== Quiz Questions ===")
    # print(result["quiz"])

    # print("\n=== Answer Key ===")
    # print(result["answer-key"])


    # Write lecture notes
    with open(f"./generated-files/{topic_name}_notes.tex", "w", encoding="utf-8") as f:
        f.write(wrap_latex(preamble, result["notes"]))

    # Write quiz
    with open(f"./generated-files/{topic_name}_quiz.tex", "w", encoding="utf-8") as f:
        f.write(wrap_latex(preamble, result["quiz"]))

    with open(f"./generated-files/{topic_name}_answer_key.tex", "w", encoding="utf-8") as f:
        f.write(wrap_latex(preamble, result["answer-key"]))

    for suffix in ["notes", "quiz", "answer_key"]:
        tex_file = f"./generated-files/{topic_name}_{suffix}.tex"
        compile_tex_to_pdf(tex_file)

    # Generate Anki deck from response
    generate_anki_deck(result["flashcards"], topic_name)


if __name__ == "__main__":
    while True:
        print("\n📚 LECTURE ASSISTANT 📚")
        print("Generate supplemental materials")
        print("Press Enter to skip.")
        print("Type 'exit' anytime to quit.")

        pdf_path = input("Name of the lecture slides (.pdf): ").strip()
        if pdf_path.lower() == "exit": break

        audio_path = input("Name of the lecture recording (video or audio): ").strip()
        if audio_path.lower() == "exit": break

        topic = input("Topic name for output files (default: 'lecture'): ").strip()
        if topic.lower() == "exit": break
        if not topic:
            topic = "lecture"

        process(
            pdf_path=pdf_path if pdf_path else None,
            audio_path=audio_path if audio_path else None,
            topic_name=topic
        )
