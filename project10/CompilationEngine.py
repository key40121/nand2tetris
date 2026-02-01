import sys
import JackTokenizer

class CompilationEngine:
    def __init__(self, tokenizer, output_stream):
        self.tokenizer = tokenizer
        self.output_stream = output_stream
        self.indent_level = 0

    def write(self, content):
        indent = '  ' * self.indent_level
        self.output_stream.write(f"{indent}{content}\n")

    def compile_class(self):
        self.write("<class>")
        self.indent_level += 1

        self.write(f"<keyword> {self.tokenizer.keyword()} </keyword>")  # 'class'
        self.tokenizer.advance()
        self.write(f"<identifier> {self.tokenizer.identifier()} </identifier>")  # class name
        self.tokenizer.advance()
        self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # '{'
        self.tokenizer.advance()

        while self.tokenizer.token_type() in JackTokenizer.TokenType.KEYWORD and self.tokenizer.keyword() in ['static', 'field']:
            self.compile_class_var_dec()
        while self.tokenizer.token_type() in JackTokenizer.TokenType.KEYWORD and self.tokenizer.keyword() in ['constructor', 'function', 'method']:
            self.compile_subroutine()
        self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # '}'
        self.indent_level -= 1
        self.write("</class>")
      
    def compile_class_var_dec(self):
        return
    
    def compile_subroutine(self):
        return
    
    def compile_parameter_list(self):
        return
    
    def compile_subroutine_body(self):
        return
    
    def compile_var_dec(self):
        return
    
    def compile_statements(self):
        return
    
    def compile_let(self):
        self.write("<letStatement>")
        self.indent_level += 1
        self.write(f"<keyword> {self.tokenizer.keyword()} </keyword>")  # 'let'
        self.tokenizer.advance()
        self.write(f"<identifier> {self.tokenizer.identifier()} </identifier>")  # varName
        self.tokenizer.advance()
        if self.tokenizer.token_type() == 'symbol' and self.tokenizer.symbol() == '[':
            self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # '['
            self.tokenizer.advance()
            self.compile_expression()
            self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # ']'
            self.tokenizer.advance()
        self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # '='
        self.tokenizer.advance()
        self.compile_expression()
        self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # ';'
        self.tokenizer.advance()
        self.indent_level -= 1
        self.write("</letStatement>")
        return
    
    def compile_if(self):
        return
    
    def compile_while(self):
        return
  
    def compile_do(self):
        return
    
    def compile_return(self):
        self.write("<returnStatement>")
        self.indent_level += 1
        self.write(f"<keyword> {self.tokenizer.keyword()} </keyword>")  # 'return'
        self.tokenizer.advance()
        if self.tokenizer.token_type() != 'symbol' or self.tokenizer.symbol() != ';':
            self.compile_expression()
        self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # ';'
        self.tokenizer.advance()
        self.indent_level -= 1
        self.write("</returnStatement>")
        return
    
    def compile_expression(self):
        return
    
    def compile_term(self):
        self.write("<term>")
        self.indent_level += 1
        token_type = self.tokenizer.token_type()
        if token_type == 'int_const':
            self.write(f"<integerConstant> {self.tokenizer.int_val()} </integerConstant>")
            self.tokenizer.advance()
        elif token_type == 'string_const':
            self.write(f"<stringConstant> {self.tokenizer.string_val()} </stringConstant>")
            self.tokenizer.advance()
        elif token_type == 'keyword':
            self.write(f"<keyword> {self.tokenizer.keyword()} </keyword>")
            self.tokenizer.advance()
        elif token_type == 'identifier':
            self.write(f"<identifier> {self.tokenizer.identifier()} </identifier>")
            self.tokenizer.advance()
            if self.tokenizer.token_type() == 'symbol' and self.tokenizer.symbol() == '[':
                self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # '['
                self.tokenizer.advance()
                self.compile_expression()
                self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # ']'
                self.tokenizer.advance()
            elif self.tokenizer.token_type() == 'symbol' and self.tokenizer.symbol() in ('(', '.'):
                if self.tokenizer.symbol() == '.':
                    self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # '.'
                    self.tokenizer.advance()
                    self.write(f"<identifier> {self.tokenizer.identifier()} </identifier>")  # subroutineName
                    self.tokenizer.advance()
                self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # '('
                self.tokenizer.advance()
                self.compile_expression_list()
                self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # ')'
                self.tokenizer.advance()
        elif token_type == 'symbol' and self.tokenizer.symbol() == '(':
            self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # '('
            self.tokenizer.advance()
            self.compile_expression()
            self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # ')'
            self.tokenizer.advance()
        elif token_type == 'symbol' and self.tokenizer.symbol() in ('-', '~'):
            self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # unaryOp
            self.tokenizer.advance()
            self.compile_term()
        return
    
    def compile_expression_list(self):
        return