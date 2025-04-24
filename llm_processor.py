import json
from groq import Groq
import re
from dotenv import load_dotenv

class GroqProcessor:
    def __init__(self, client: Groq):
        self.client = client
        self.system_prompt = f"""You are a precise AI assistant that generates structured academic content from lecture transcripts and slides. You must return a **valid JSON object** using the schema below.

        The JSON must contain:
        1. `notes`: Very detailed LaTeX-formatted lecture notes, notes should be written at a college-level (no preamble)
        2. `quiz`: Exactly 10 multiple-choice questions, derived from the input material (LaTeX)
        3. `answer-key`: Correct answers for ALL quiz questions (LaTeX)
        4. `flashcards`: JSON array of front/back string pairs

        Here is the schema:
        {json.dumps({
            "type": "object",
            "properties": {
                "notes": {"type": "string"},
                "quiz": {"type": "string"},
                "answer-key": {"type": "string"},
                "flashcards": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {"front": {"type": "string"}, "back": {"type": "string"}},
                        "required": ["front", "back"]
                    }
                }
            },
            "required": ["notes", "quiz", "answer-key", "flashcards"]
        }, indent=2)}

        --- LaTeX Formatting Rules ---

        --- NOTES ---
        - Must be a valid LaTeX document with:
        - `\\begin{{document}}` and `\\end{{document}}`
        - `\\section{{}}`, `\\subsection{{}}`, `\\subsubsection{{}}` for hierarchy
        - Definitions labeled with `\\textbf{{Definition:}}`, claims with `\\textbf{{Claim:}}`, and proofs with `\\textit{{Proof:}}`
        - Use `\\begin{{itemize}}` or `\\begin{{enumerate}}` for bullets
        - Math formatted properly with `$...$` for inline and `\\[...\\]` for display
        - Emphasize keywords (`\\textbf`, `\\textit`) and use spacing (`\\vspace`, `\\noindent`) to improve readability
        - Mimic clean, human-written academic notes. No AI-generic structure or plain walls of text

        --- QUIZ ---
        - MUST be a valid LaTeX document containing *EXACTLY 10* multiple choice questions with:
        - '\\begin{{document}}' at the start of the contents
        - Exactly 10 multiple-choice questions using:
        - `\\begin{{enumerate}}`
        - After the 10 questions, make sure to end the quiz with:
        - '\\end{{enumerate}}'
        - Each question must have four answer choices: (A), (B), (C), (D)
        - Each answer choice should be valid and relevant to the question
        - Each question should be styled as follows:
            - '\\item (question)'
            - '\\begin{{enumerate}}'
            - '\\item[A] (answer choice A)'
            - '\\item[B] (answer choice B)'
            - '\\item[C] (answer choice C)'
            - '\\item[D] (answer choice D)'
            - '\\end{{enumerate}}'
            - Newline
        - All questions must be answerable from the input material and written at a college difficulty level
        - Must be a valid LaTeX document with:
        - '\\end{{document}}' at the end of the contents

        --- ANSWER KEY ---
        - Must be a valid LaTeX document with:
        - '\\begin{{document}}' and '\\end{{document}}'
        - Must always include an answer key that directly follows the quiz questions.
        - Use `\\newpage` to begin answer key
        - List answers clearly: `1. (B)`, `2. (C)`, … `10. (A)`
        - Each answer should be styled as follows:
            - '\\item[(question number)] (correct answer choice)'
        - Answers should be correct and accurate
        - Must include all 10 answers and be easy to match back to the quiz

        --- FLASHCARDS ---
        - Maintain current format: JSON array with "front" and "back" strings

        --- GENERAL ---
        - No Markdown or Unicode symbols (e.g., use `\\alpha` instead of α)
        - Do not output anything except the valid JSON object
        - Do not include LaTeX preamble; this is added later
        - REQUIRED: Must generate exactly 10 questions for the quiz 
        - REQURIED: Must generate exactly 4 answer choices for each quiz question: (A), (B), (C), (D)
        - REQUIRED: Each answer choice must be its own LaTeX item 
        - REQUIRED: Answer key always contains correct answers for the 10 questions in the quiz.
        - REQUIRED: Be sure to generate the full, complete LaTeX documents for the notes, quiz, answer key, and flashcards
        - REQUIRED: Quiz questions and answer key should always adhere exactly to the specified style
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