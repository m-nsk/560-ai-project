import pdfkit
import markdown2
import re
import os

def slugify(title):
    return re.sub(r'[^a-zA-Z0-9_-]', '_', title.strip().lower())

def escape_latex(text):
    """Wrap LaTeX math in backticks to format visibly if not rendered."""
    return re.sub(r'(\$[^\$]*\$)', r'`\1`', text)

def notes_to_pdf(notes: list):
    # Combine notes into markdown
    markdown_text = ""
    for note in notes:
        content = note["content"].strip()
        content = escape_latex(content)

        if note["title"].strip() not in content:
            markdown_text += f"# {note['title']}\n\n"

        markdown_text += content + "\n\n"

    markdown_text = markdown_text.strip()

    # Convert markdown to HTML
    html_body = markdown2.markdown(markdown_text, extras=["fenced-code-blocks", "tables"])

    # HTML wrapper with reduced bottom margin to avoid blank pages
    html_template = f"""
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{
                font-family: 'Georgia', serif;
                margin: 1in;
                margin-bottom: 0.5in;  /* prevent extra blank page */
                line-height: 1.75;
                color: #2c3e50;
            }}
            h1 {{
                font-size: 32px;
                font-weight: bold;
                color: #1a1a1a;
                margin-top: 1.5em;
                margin-bottom: 0.5em;
                border-bottom: 2px solid #ccc;
            }}
            h2 {{
                font-size: 24px;
                color: #333;
                margin-top: 1.25em;
                margin-bottom: 0.4em;
            }}
            h3 {{
                font-size: 20px;
                color: #555;
                margin-top: 1em;
                margin-bottom: 0.4em;
            }}
            p {{
                margin-bottom: 1em;
            }}
            pre, code {{
                background: #f4f4f4;
                padding: 0.4em;
                border-radius: 4px;
                font-family: Consolas, monospace;
            }}
            ul, ol {{
                margin-left: 1.25em;
                margin-bottom: 1em;
            }}
        </style>
    </head>
    <body>
        {html_body}
    </body>
    </html>
    """.strip()  # Strip trailing whitespace

    # Save HTML to temp file
    html_path = "notes_temp.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_template)

    # Create output directory
    output_dir = os.path.join(os.getcwd(), "note-pdfs")
    os.makedirs(output_dir, exist_ok=True)

    # Final output file
    output_filename = os.path.join(output_dir, f"{slugify(notes[0]['title'])}.pdf")

    # Convert to PDF
    pdfkit.from_file(html_path, output_filename)
    print(f"PDF saved as {output_filename}")

    # Cleanup
    os.remove(html_path)
