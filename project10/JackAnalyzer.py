import JackTokenizer
import CompilationEngine

def main():
  print("Hello, Jack Analyzer!")

  jack_tokenizer = JackTokenizer.JackTokenizer("./ExpressionLessSquare/Square.jack")
  compilation_engine = CompilationEngine.CompilationEngine(jack_tokenizer, open("./ExpressionLessSquare/Square_test.xml", "w"))

  while jack_tokenizer.has_more_tokens():
    jack_tokenizer.advance()
    compilation_engine.compile_class()

if __name__ == "__main__":
  main()