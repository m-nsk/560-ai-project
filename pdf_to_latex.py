import os, subprocess

def compile_tex_to_pdf(tex_path: str):
    directory = os.path.dirname(tex_path)
    filename = os.path.basename(tex_path)
    base_name = os.path.splitext(filename)[0]
    
    try:
        # Compile twice to resolve references
        for _ in range(2):
            subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", filename],
                cwd=directory,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        print(f"Compiled: {tex_path}")
        
        # Clean up auxiliary files
        for ext in [".aux", ".log", ".out"]:
            aux_file = os.path.join(directory, base_name + ext)
            if os.path.exists(aux_file):
                os.remove(aux_file)
        
    except Exception as e:
        print(f"Failed to compile {tex_path}: {e}")
