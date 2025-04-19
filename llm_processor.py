import json
from groq import Groq
import re
from dotenv import load_dotenv

class GroqProcessor:
    def __init__(self, client: Groq):
        self.client = client
        self.system_prompt = f"""You are a helpful AI assistant that creates detailed, structured educational content from lecture transcripts and/or slides.
        You must return a valid JSON object that adheres to the following schema:
        {json.dumps({
            "type": "object",
            "properties": {
                "notes": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string"},
                            "content": {
                                "type": "string",
                                "description": "Markdown-formatted content with proper structure"
                            }
                        },
                        "required": ["title", "content"]
                    }
                },
                "quiz": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "question": {"type": "string"},
                            "options": {
                                "type": "array",
                                "items": {"type": "string"}
                            },
                            "correct_answer": {"type": "string"}
                        },
                        "required": ["question", "options", "correct_answer"]
                    }
                },
                "flashcards": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "front": {"type": "string"},
                            "back": {"type": "string"}
                        },
                        "required": ["front", "back"]
                    }
                }
            },
            "required": ["notes", "quiz", "flashcards"]
        }, ensure_ascii=False, indent=2)}
        
        Generate detailed and lengthy notes based on what the lecturer talks about in the lecture transcript and lecture slides (if they are provided).
        The notes should take up most of the response, as it is the most important feature.
        
        Generate at least 10 quiz questions.
        Generate flash cards based on keywords in the lecture.

        Instructions for formatting:
        - Notes should use **Markdown syntax**:
        - Use `#` for main headings and `##` for subheadings
        - Use `-` for bullet points
        - Use triple backticks (```) for code blocks
        - Use LaTeX formatting, `**bold**`, `*italic*`, and `> blockquotes` when appropriate

        Assume some errors or omissions may exist in slide content (e.g., missing tables, graphs). Use best judgment to infer or reconstruct meaning if necessary.

        Do not include any explanation, preamble, or extra text—only return a valid JSON object matching the above schema.
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
            temperature=0.5,
            max_completion_tokens=8192,
            top_p=1,
            stream=False,
            response_format={"type": "json_object"},
            stop=["}END_JSON"],
        )

        try:
            return json.loads(completion.choices[0].message.content)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON response: {e}\nResponse content: {completion.choices[0].message.content}")