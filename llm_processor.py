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

        --- LaTeX Formatting Rules, Document Layout, and Document Contents Specifications ---

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
        - MUST be a valid LaTeX document containing *EXACTLY 10* multiple choice questions
        - Each question must have four answer choices: (A), (B), (C), (D)
        - Each answer choice should be valid and relevant to the question
        - Each question should be styled as follows:
        - All questions must be answerable from the input material and written at a college difficulty level
        - The quiz document should be strictly styled as follows, only fill in the questions and the answer choices:
            - '\\begin{{document}}'
            - '\\begin{{enumerate}}'
            - '\\item (Question 1)'
            - '\\begin{{enumerate}}'
            - '\\item[A] (question 1 answer choice A)'
            - '\\item[B] (question 1 answer choice B)'
            - '\\item[C] (question 1 answer choice C)'
            - '\\item[D] (question 1 answer choice D)'
            - '\\end{{enumerate}}'
            - newline
            - '\\item (Question 2)'
            - '\\begin{{enumerate}}'
            - '\\item[A] (question 2 answer choice A)'
            - '\\item[B] (question 2 answer choice B)'
            - '\\item[C] (question 2 answer choice C)'
            - '\\item[D] (question 2 answer choice D)'
            - '\\end{{enumerate}}'
            - newline
            - '\\item (Question 3)'
            - '\\begin{{enumerate}}'
            - '\\item[A] (question 3 answer choice A)'
            - '\\item[B] (question 3 answer choice B)'
            - '\\item[C] (question 3 answer choice C)'
            - '\\item[D] (question 3 answer choice D)'
            - '\\end{{enumerate}}'
            - newline
            - '\\item (Question 4)'
            - '\\begin{{enumerate}}'
            - '\\item[A] (question 4 answer choice A)'
            - '\\item[B] (question 4 answer choice B)'
            - '\\item[C] (question 4 answer choice C)'
            - '\\item[D] (question 4 answer choice D)'
            - '\\end{{enumerate}}'
            - newline
            - '\\item (Question 5)'
            - '\\begin{{enumerate}}'
            - '\\item[A] (question 5 answer choice A)'
            - '\\item[B] (question 5 answer choice B)'
            - '\\item[C] (question 5 answer choice C)'
            - '\\item[D] (question 5 answer choice D)'
            - '\\end{{enumerate}}'
            - newline
            - '\\item (Question 6)'
            - '\\begin{{enumerate}}'
            - '\\item[A] (question 6 answer choice A)'
            - '\\item[B] (question 6 answer choice B)'
            - '\\item[C] (question 6 answer choice C)'
            - '\\item[D] (question 6 answer choice D)'
            - '\\end{{enumerate}}'
            - newline
            - '\\item (Question 7)'
            - '\\begin{{enumerate}}'
            - '\\item[A] (question 7 answer choice A)'
            - '\\item[B] (question 7 answer choice B)'
            - '\\item[C] (question 7 answer choice C)'
            - '\\item[D] (question 7 answer choice D)'
            - '\\end{{enumerate}}'
            - newline
            - '\\item (Question 8)'
            - '\\begin{{enumerate}}'
            - '\\item[A] (question 8 answer choice A)'
            - '\\item[B] (question 8 answer choice B)'
            - '\\item[C] (question 8 answer choice C)'
            - '\\item[D] (question 8 answer choice D)'
            - '\\end{{enumerate}}'
            - newline
            - '\\item (Question 9)'
            - '\\begin{{enumerate}}'
            - '\\item[A] (question 9 answer choice A)'
            - '\\item[B] (question 9 answer choice B)'
            - '\\item[C] (question 9 answer choice C)'
            - '\\item[D] (question 9 answer choice D)'
            - '\\end{{enumerate}}'
            - newline
            - '\\item (Question 10)'
            - '\\begin{{enumerate}}'
            - '\\item[A] (question 10 answer choice A)'
            - '\\item[B] (question 10 answer choice B)'
            - '\\item[C] (question 10 answer choice C)'
            - '\\item[D] (question 10 answer choice D)'
            - '\\end{{enumerate}}'
            - '\\end{{enumerate}}'
            - '\\end{{document}}'
        - Quiz document should be structured exactly as specified, do not add or remove anything, only fill in the information from the input materials.


        --- ANSWER KEY ---
        - Must be a valid LaTeX document
        - Must always include an answer key that directly follows the quiz questions.
        - List answers clearly: `1. (B)`, `2. (C)`, … `10. (A)`
        - Answers should be correct and accurate
        - Must include all 10 answers and be easy to match back to the quiz
        - The answer-key document should be strictly styled as follows, only fill in the correct answers to the corresponding questions:
            - '\\begin{{document}}'
            - '\\newpage'
            - '\\begin{{enumerate}}'
            - '\\item[1] (Correct answer choice for quiz question 1)'
            - '\\item[2] (Correct answer choice for quiz question 2)'
            - '\\item[3] (Correct answer choice for quiz question 3)'
            - '\\item[4] (Correct answer choice for quiz question 4)'
            - '\\item[5] (Correct answer choice for quiz question 5)'
            - '\\item[6] (Correct answer choice for quiz question 6)'
            - '\\item[7] (Correct answer choice for quiz question 7)'
            - '\\item[8] (Correct answer choice for quiz question 8)'
            - '\\item[9] (Correct answer choice for quiz question 9)'
            - '\\item[10] (Correct answer choice for quiz question 10)'
            - '\\end{{enumerate}}'
            - '\\end{{document}}'
        - Answer-key document should be structured exactly as specified, do not add or remove anything, only fill in the correct answers to the questions

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
        - REQUIRED: Notes, quiz, answer-key, and flashcards should always adhere exactly to the specified style
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