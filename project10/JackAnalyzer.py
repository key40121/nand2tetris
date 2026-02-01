import JackTokenizer

def main():
  print("Hello, Jack Analyzer!")

  jack_tokenizer = JackTokenizer.JackTokenizer("./ArrayTest/Main.jack")

  while jack_tokenizer.has_more_tokens():
    jack_tokenizer.advance()
    if jack_tokenizer.token_type() == JackTokenizer.TokenType.KEYWORD:
      print("KEYWORD: ", jack_tokenizer.keyword())
    elif jack_tokenizer.token_type() == JackTokenizer.TokenType.SYMBOL:
      print("SYMBOL: ", jack_tokenizer.symbol())
    elif jack_tokenizer.token_type() == JackTokenizer.TokenType.IDENTIFIER:
      print("IDENTIFIER: ", jack_tokenizer.identifier())
    elif jack_tokenizer.token_type() == JackTokenizer.TokenType.INT_CONST:
      print("INT_CONST: ", jack_tokenizer.int_val())
    elif jack_tokenizer.token_type() == JackTokenizer.TokenType.STRING_CONST:
      print("STRING_CONST: ", jack_tokenizer.string_val())
if __name__ == "__main__":
  main()