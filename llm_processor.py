import json
from groq import Groq
import re
from dotenv import load_dotenv

class GroqProcessor:
    def __init__(self, client: Groq):
        self.client = client
        self.system_prompt = f"""You are a helpful AI assistant that creates structured educational content from lecture transcripts and/or slides.
        You must return a valid JSON object that adheres to the following schema:
        {json.dumps({
            "type": "object",
            "properties": {
                "notes": {
                    "type": "string",
                    "description": "A complete LaTeX document EXCLUDING the preamble that contains detailed lecture notes. DO NOT USE MARKDOWN. WE ARE USING LATEX."
                },
                "quiz": {
                    "type": "string",
                    "description": "A complete LaTeX document EXCLUDING the preamble that contains a multiple choice quiz with at least 10 questions"
                },
                "answer-key": {
                    "type": "string",
                    "description": "A complete LaTeX document EXCLUDING the preamble that contains answers to the multiple choice quiz above"
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

        Instructions:
        - Return a **valid JSON object** with three top-level keys: `notes`, `quiz`, `answer-key`, and `flashcards`.
        - `notes` and `quiz` must each be a **LaTeX document**, starting with `\\begin{{document}}` and `\\end{{document}}`.
        - Use proper LaTeX formatting:
        - NO SPECIAL UNICODE CHARACTERS. If you encounter characters like α, use the latex version \\alpha.
        - `\\section{{}}`, `\\subsection{{}}` for structure
        - `\\begin{{itemize}}` or `\\begin{{enumerate}}` for lists
        - `$...$` or `\\[ ... \\]` for math
        - Use `\\textbf{{}}`, `\\textit{{}}`, `\\begin{{quote}}`, etc. for emphasis
        - For the **quiz**, include EXACTLY 10 multiple choice questions using `enumerate`, with lettered choices (A, B, C...). Then on a new page, write out the answers to each problem.
        - Flashcards should remain a structured array of front/back string pairs.
        - Do not include any explanation, comments, or preamble outside the JSON object.
        - This is the preamble that is already provided:
        ```latex
        \\documentclass[11pt]{{article}}
        \\usepackage[utf8]{{inputenc}}
        \\usepackage{{amsmath, amssymb}}
        \\usepackage{{enumitem}}
        \\usepackage{{graphicx}}
        \\usepackage{{geometry}}
        \\usepackage{{hyperref}}
        \\usepackage{{xcolor}}

        \\geometry{{margin=1in}}
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