import json
from groq import Groq
import re
from dotenv import load_dotenv

class GroqProcessor:
    def __init__(self, client: Groq):
        self.client = client
        self.system_prompt = """You are a helpful AI assistant that creates educational content from lecture transcripts. 
        Your task is to create a structured JSON output containing:
        1. Detailed notes from the lecture (in markdown format). Follow along and generate in-depth notes for important concepts covered by the professor.
        2. 10 or more questions based on the content
        3. Flashcards for important concepts
        
        Be as helpful as possible.
        
        Format your response as a valid JSON object with the following structure:
        {
            "notes": [{"title": "string", "content": "markdown string with proper formatting (headings, lists, code blocks, etc.)"}],
            "quiz": [{"question": "string", "options": ["string"], "correct_answer": "string"}],
            "flashcards": [{"front": "string", "back": "string"}]
        }

        
        Note that the slides conversion may contain errors in objects like tables, images, and graphs. Assume the content appropriately in case of errors.

        For the notes content, use markdown formatting.
        """

    @staticmethod
    def sanitize_input(text: str) -> str:
        text = text.replace("\u200b", "")  # Remove zero-width spaces
        text = re.sub(r'\\', '', text)     # Remove stray backslashes
        return text.strip()

    def process_transcript(self, transcript: str | None = None, slides: str | None = None) -> dict:
        if transcript is None and slides is None:
            raise ValueError("At least one of transcript or slides must be provided")
            
        # Prepare the content for the prompt
        content_parts = []
        if transcript is not None:
            content_parts.append(f"Transcript of the lecture:\n{self.sanitize_input(transcript)}")
            print("Using transcript")
        if slides is not None:
            content_parts.append(f"Slides from the lecture:\n{self.sanitize_input(slides)}")
            print("Using slides")
            
        content = "\n\n".join(content_parts)
            
        completion = self.client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[
                {"role": "system", "content": self.system_prompt},
                {
                    "role": "user",
                    "content": f"Based on the following lecture content, generate ONLY a VALID JSON object with three top-level keys: 'notes', 'quiz', and 'flashcards'.\n\nDo not include explanations or preambles. Your entire response must be valid JSON.\n\nLecture content:\n\n{content}"
                }
            ],
            temperature=1,
            max_completion_tokens=1024,
            top_p=1,
            stream=False,
            response_format={"type": "json_object"},
            stop=None,
        )

        try:
            return json.loads(completion.choices[0].message.content)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON response: {e}\nResponse content: {completion.choices[0].message.content}")