# LectureMate: An LLM-Powered Educational Material Processor
### Final Project for COMP 560: Artificial Intelligence | Connor Hall, Lucas Jorgensen, Minjae Kung
**An AI-powered educational tool that transforms lecture materials into comprehensive study guides**

## Overview

This project demonstrates a pipeline for processed lecture content (audio/video recordings and PDF slides) using Large Language Models (LLMs) to generate valuable study resources for students. By leveraging the Groq API for fast inference and local/cloud-based transcription services, this tool automates the creation of:

*   **Detailed Notes**: Structured markdown notes summarizing key concepts from lectures.
*   **Quiz Questions**: Multiple-choice questions to test understanding.
*   **Anki Flashcards**: Ready-to-import `.apkg` decks for spaced repetition learning.

## Features

1.  **Multi-Modal Input Processing**:
    *   **Audio Transcription**: Uses OpenAI's Whisper (local) or Groq's Whisper API (cloud) to transcribe lecture audio with high accuracy.
    *   **Slide Extraction**: Converts PDF lecture slides into text/markdown using `pymupdf4llm` to provide visual context to the LLM.

2.  **Intelligent Content Generation**:
    *   Synthesizes information from both the transcript and slides.
    *   Uses **Meta-Llama 3** (via Groq) to generate structured educational content.
    *   Produces output in a strict JSON schema for reliable parsing.

3.  **Automated Flashcard Creation**:
    *   Extracts key terms and definitions.
    *   Generates an Anki deck (`.apkg`) automatically using `genanki`.

## Architecture

The pipeline consists of the following modules:

*   `main.py`: The orchestrator that manages the data flow from input to output.
*   `transcriber.py`: Handles audio transcription using either local Whisper models or the Groq API.
*   `llm_processor.py`: Interfaces with the Groq API to process text and generate the JSON response containing notes, quizzes, and flashcards.
*   `flashcards_maker.py`: Takes the generated flashcard data and compiles it into an Anki deck.

## Setup & Installation

### Prerequisites

*   Python 3.8+
*   A [Groq API Key](https://console.groq.com/)

### Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/yourusername/560-ai-project-1.git
    cd 560-ai-project-1
    ```

2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    pip install groq python-dotenv openai-whisper
    # Note: openai-whisper requires ffmpeg to be installed on your system
    ```

3.  Set up environment variables:
    Create a `.env` file in the root directory:
    ```env
    GROQ_API_KEY=your_groq_api_key_here
    ```

## Usage

Currently, the Proof of Concept is set up to process sample files located in the `test-files` directory.

1.  Place your lecture audio (e.g., `.mp3`) and slides (e.g., `.pdf`) in the `test-files` directory.
2.  Update the file paths in `main.py` to point to your specific files.
3.  Run the main script:
    ```bash
    python main.py
    ```

The script will output the generated notes and quiz questions to the console and save an Anki deck (e.g., `lecture.apkg`) to the `anki-decks` folder.

## Future Improvements

*   **User Interface**: Develop a web-based frontend for easy file upload and management.
*   **Vector Database**: Implement RAG (Retrieval-Augmented Generation) for handling larger courses and querying across multiple lectures.
*   **Output Formats**: Support exporting notes to PDF or Notion.

Note: This is a Proof of Concept (POC) designed for educational purposes. It is currently configured for demonstration with specific test files.