import sys
import os
from pathlib import Path
import JackTokenizer
import CompilationEngine

def compile_jack_file(jack_file_path, output_file_path):
    """Runnable task that compiles a single .jack file into an XML file."""
    jack_tokenizer = JackTokenizer.JackTokenizer(jack_file_path)
    with open(output_file_path, "w") as output_file:
        compilation_engine = CompilationEngine.CompilationEngine(jack_tokenizer, output_file)
        if jack_tokenizer.has_more_tokens():
            jack_tokenizer.advance()
            compilation_engine.compile_class()

def main():
    if len(sys.argv) != 2:
        print("Usage: JackAnalyzer.py <file.jack or directory>")
        return
    
    input_path = sys.argv[1]
    path = Path(input_path)
    
    if path.is_dir():
        jack_files = sorted(path.glob("*.jack"))
        if not jack_files:
            print(f"No .jack files found in {input_path}")
            return
        
        for jack_file in jack_files:
            output_file = jack_file.with_suffix(".xml")
            print(f"Compiling {jack_file.name} -> {output_file.name}")
            compile_jack_file(str(jack_file), str(output_file))
    
    elif path.is_file() and path.suffix == ".jack":
        # Single file mode
        output_file = path.with_suffix(".xml")
        print(f"Compiling {path.name} -> {output_file.name}")
        compile_jack_file(str(path), str(output_file))
    
    else:
        print("Error: Input must be a .jack file or a directory")
        return

if __name__ == "__main__":
    main()