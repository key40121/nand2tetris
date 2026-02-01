from enum import Enum
import sys
import re

class TokenType(Enum):
    KEYWORD = 1
    SYMBOL = 2
    IDENTIFIER = 3
    INT_CONST = 4
    STRING_CONST = 5

class Keyword(Enum):
    CLASS = "class"
    METHOD = "method"
    FUNCTION = "function"
    CONSTRUCTOR = "constructor"
    INT = "int"
    BOOLEAN = "boolean"
    CHAR = "char"
    VOID = "void"
    VAR = "var"
    STATIC = "static"
    FIELD = "field"
    LET = "let"
    DO = "do"
    IF = "if"
    ELSE = "else"
    WHILE = "while"
    RETURN = "return"
    TRUE = "true"
    FALSE = "false"
    NULL = "null"
    THIS = "this"

class JackTokenizer:
    def __init__(self, input_file, encoding='utf-8'):
        """
        Initializes the tokenizer with the input file.
        This class handles tokenizing a Jack source file.
        """
        with open(input_file, 'r', encoding=encoding) as f:
          self.file = f.read()
        self.tokens = []
        self.current_token = None
        self.remove_comments_and_whitespace()
        self.tokenize()

    def remove_comments_and_whitespace(self):
        """
        Removes comments and leading/trailing whitespace from a line.
        """
        # remove /* ... */ comments
        self.file = re.sub(r'/\*.*?\*/', '', self.file, flags=re.S)
        # remove // comments
        self.file = re.sub(r'//.*', '', self.file)
        return
    
    def tokenize(self):
        """
        Tokenizes the input file into a list of tokens.
        """
        TOKEN_REGEX = re.compile(
            r'"[^"\n]*"'            # string constant
            r'|\d+'                 # integer constant
            r'|[A-Za-z_]\w*'        # identifier or keyword
            r'|[{}\(\)\[\].,;+\-*/&|<>=~]'  # symbols
        )

        self.tokens = TOKEN_REGEX.findall(self.file)
        return

    def has_more_tokens(self) -> bool:
        """
        Checks if there are more tokens in the input.
        ignore comments and whitespace.
        """
        if self.tokens:
            return True
        else:
            return False

    def advance(self) -> None:
        if self.tokens:
            self.current_token = self.tokens.pop(0)

    def token_type(self) -> TokenType:
        
        KEYWORDS = {
            "class", "method", "function", "constructor", "int", "boolean", "char", "void",
            "var", "static", "field", "let", "do", "if", "else", "while", "return",
            "true", "false", "null", "this"
        }

        SYMBOLS = set("{}()[].,;+-*/&|<>=~")

        if self.current_token in KEYWORDS:
            return TokenType.KEYWORD

        if self.current_token in SYMBOLS:
            return TokenType.SYMBOL
        
        if self.current_token.isdigit():
            return TokenType.INT_CONST

        if self.current_token.startswith('"') and self.current_token.endswith('"'):
            return TokenType.STRING_CONST
        
        return TokenType.IDENTIFIER

    def keyword(self) -> str:
        if self.token_type() == TokenType.KEYWORD:
            for kw in Keyword:
                if self.current_token == kw.value:
                    return kw.value
    
    def symbol(self) -> str:
        if self.token_type() == TokenType.SYMBOL:
          return self.current_token

    def identifier(self) -> str:
        if self.token_type() == TokenType.IDENTIFIER:
            return self.current_token
    
    def int_val(self) -> int:
        if self.token_type() == TokenType.INT_CONST:
            return int(self.current_token)
    
    def string_val(self) -> str:
        if self.token_type() == TokenType.STRING_CONST:
            return self.current_token[1:-1]  # remove the surrounding quotes