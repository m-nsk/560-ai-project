from groq import Groq
import os
from dotenv import load_dotenv

class GroqProcessor:
    def __init__(self):
        load_dotenv()
        self.client = Groq()
        self.system_prompt = """You are a helpful AI assistant that creates educational content from lecture transcripts. 
        Your task is to create a structured JSON output containing:
        1. Key notes from the lecture (in markdown format)
        2. Quiz questions based on the content
        3. Flashcards for important concepts
        
        Format your response as a valid JSON object with the following structure:
        {
            "notes": [{"title": "string", "content": "markdown string with proper formatting (headings, lists, code blocks, etc.)"}],
            "quiz": [{"question": "string", "options": ["string"], "correct_answer": "string"}],
            "flashcards": [{"front": "string", "back": "string"}]
        }

        For the notes content, use markdown formatting:
        - Use # for main headings
        - Use ## for subheadings
        - Use bullet points (-) for lists
        - Use ``` for code blocks
        - Use ** for bold text
        - Use * for italic text
        - Use > for blockquotes
        """

    def process_transcript(self, transcript: str) -> str:
        completion = self.client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[
                {"role": "system", "content": self.system_prompt},
                {
                    "role": "user",
                    "content": f"Create a .json that contains notes, quiz, and flashcard objects based on the transcript of a lecture provided here: {transcript}"
                }
            ],
            temperature=1,
            max_completion_tokens=1024,
            top_p=1,
            stream=True,
            stop=None,
        )

        full_response = ""
        for chunk in completion:
            content = chunk.choices[0].delta.content or ""
            full_response += content
            print(content, end="")
        
        return full_response