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

        while self.tokenizer.token_type() == JackTokenizer.TokenType.KEYWORD and self.tokenizer.keyword() in ['static', 'field']:
            self.compile_class_var_dec()
        while self.tokenizer.token_type() == JackTokenizer.TokenType.KEYWORD and self.tokenizer.keyword() in ['constructor', 'function', 'method']:
            self.compile_subroutine()
        self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # '}'
        self.tokenizer.advance()
        self.indent_level -= 1
        self.write("</class>")
      
    def compile_class_var_dec(self):
        # static or field
        self.write(f"<classVarDec>")
        self.indent_level += 1
        self.write(f"<keyword> {self.tokenizer.keyword()} </keyword>")  # 'static' or 'field'
        self.tokenizer.advance()
        self.write(f"<keyword> {self.tokenizer.keyword()} </keyword>")  # type
        self.tokenizer.advance()
        self.write(f"<identifier> {self.tokenizer.identifier()} </identifier>")  # varName
        self.tokenizer.advance()
        self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # ',' or ';'
        while self.tokenizer.symbol() == ',':
            self.tokenizer.advance()
            self.write(f"<identifier> {self.tokenizer.identifier()} </identifier>")  # varName
            self.tokenizer.advance()
            self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # ',' or ';'
        self.tokenizer.advance()  # skip ';'
        self.indent_level -= 1
        self.write(f"</classVarDec>")
        return
    
    def compile_subroutine(self):
        # constructor, function, or method
        self.write("<subroutineDec>")
        self.indent_level += 1
        self.write(f"<keyword> {self.tokenizer.keyword()} </keyword>")  # 'constructor'/'function'/'method'
        self.tokenizer.advance()
        self.write(f"<keyword> {self.tokenizer.keyword()} </keyword>")  # 'void' or type
        self.tokenizer.advance()
        self.write(f"<identifier> {self.tokenizer.identifier()} </identifier>")  # subroutineName
        self.tokenizer.advance()
        self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # '('
        self.tokenizer.advance()
        self.compile_parameter_list()
        self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # ')'
        self.tokenizer.advance()
        self.compile_subroutine_body()
        self.indent_level -= 1
        self.write("</subroutineDec>")
        return
    
    def compile_parameter_list(self):
        self.write("<parameterList>")
        self.indent_level += 1
        if self.tokenizer.token_type() in [JackTokenizer.TokenType.KEYWORD, JackTokenizer.TokenType.IDENTIFIER]:
            self.write(f"<keyword> {self.tokenizer.keyword()} </keyword>")  # type
            self.tokenizer.advance()
            self.write(f"<identifier> {self.tokenizer.identifier()} </identifier>")  # varName
            self.tokenizer.advance()
            while self.tokenizer.symbol() == ',':
                self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # ','
                self.tokenizer.advance()
                self.write(f"<keyword> {self.tokenizer.keyword()} </keyword>")  # type
                self.tokenizer.advance()
                self.write(f"<identifier> {self.tokenizer.identifier()} </identifier>")  # varName
                self.tokenizer.advance()
        self.indent_level -= 1
        self.write("</parameterList>")
        return
    
    def compile_subroutine_body(self):
        self.write("<subroutineBody>")
        self.indent_level += 1
        self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # '{'
        self.tokenizer.advance()
        while self.tokenizer.token_type() == JackTokenizer.TokenType.KEYWORD and self.tokenizer.keyword() == 'var':
            self.compile_var_dec()
        self.compile_statements()
        self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # '}'
        self.tokenizer.advance()
        self.indent_level -= 1
        self.write("</subroutineBody>")
        return
    
    def compile_var_dec(self):
        self.write("<varDec>")
        self.indent_level += 1
        self.write(f"<keyword> {self.tokenizer.keyword()} </keyword>")  # 'var'
        self.tokenizer.advance()
        # Type can be keyword (int, boolean, void) or identifier (class name)
        if self.tokenizer.token_type() == JackTokenizer.TokenType.KEYWORD:
            self.write(f"<keyword> {self.tokenizer.keyword()} </keyword>")  # type
        else:
            self.write(f"<identifier> {self.tokenizer.identifier()} </identifier>")  # type (class name)
        self.tokenizer.advance()
        self.write(f"<identifier> {self.tokenizer.identifier()} </identifier>")  # varName
        self.tokenizer.advance()
        self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # ',' or ';'
        while self.tokenizer.symbol() == ',':
            self.tokenizer.advance()
            self.write(f"<identifier> {self.tokenizer.identifier()} </identifier>")  # varName
            self.tokenizer.advance()
            self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # ',' or ';'
        self.tokenizer.advance()  # skip ';'
        self.indent_level -= 1
        self.write(f"</varDec>")
        return
    
    def compile_statements(self):
        self.write("<statements>")
        self.indent_level += 1
        while self.tokenizer.token_type() == JackTokenizer.TokenType.KEYWORD and self.tokenizer.keyword() in ['let', 'if', 'while', 'do', 'return']:
            if self.tokenizer.keyword() == 'let':
                self.compile_let()
            elif self.tokenizer.keyword() == 'if':
                self.compile_if()
            elif self.tokenizer.keyword() == 'while':
                self.compile_while()
            elif self.tokenizer.keyword() == 'do':
                self.compile_do()
            elif self.tokenizer.keyword() == 'return':
                self.compile_return()
        self.indent_level -= 1
        self.write("</statements>")
        return
    
    def compile_let(self):
        self.write("<letStatement>")
        self.indent_level += 1
        self.write(f"<keyword> {self.tokenizer.keyword()} </keyword>")  # 'let'
        self.tokenizer.advance()
        self.write(f"<identifier> {self.tokenizer.identifier()} </identifier>")  # varName
        self.tokenizer.advance()
        if self.tokenizer.token_type() == JackTokenizer.TokenType.SYMBOL and self.tokenizer.symbol() == '[':
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
        self.write("<ifStatement>")
        self.indent_level += 1
        self.write(f"<keyword> {self.tokenizer.keyword()} </keyword>")  # 'if'
        self.tokenizer.advance()
        self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # '('
        self.tokenizer.advance()
        self.compile_expression()
        self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  #
        self.tokenizer.advance()
        self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # '{'
        self.tokenizer.advance()
        self.compile_statements()
        self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # '}'
        self.tokenizer.advance()
        self.indent_level -= 1
        self.write("</ifStatement>")
        return
    
    def compile_while(self):
        self.write("<whileStatement>")
        self.indent_level += 1
        self.write(f"<keyword> {self.tokenizer.keyword()} </keyword>")  # 'while'
        self.tokenizer.advance()
        self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # '('
        self.tokenizer.advance()
        self.compile_expression()
        self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # ')'
        self.tokenizer.advance()
        self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  #
        self.tokenizer.advance()
        self.compile_statements()
        self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # '}'
        self.tokenizer.advance()
        self.indent_level -= 1
        self.write("</whileStatement>")
        return
  
    def compile_do(self):
        self.write("<doStatement>")
        self.indent_level += 1
        self.write(f"<keyword> {self.tokenizer.keyword()} </keyword>")  # 'do'
        self.tokenizer.advance()
        self.write(f"<identifier> {self.tokenizer.identifier()} </identifier>")  # subroutineName or className or varName
        self.tokenizer.advance()
        if self.tokenizer.token_type() == JackTokenizer.TokenType.SYMBOL and self.tokenizer.symbol() == '.':
            self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # '.'
            self.tokenizer.advance()
            self.write(f"<identifier> {self.tokenizer.identifier()} </identifier>")  # subroutineName
            self.tokenizer.advance()
        self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # '('
        self.tokenizer.advance()
        self.compile_expression_list()
        self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # ')'
        self.tokenizer.advance()  # consume ')'
        self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # ';'
        self.tokenizer.advance()  # consume ';'
        self.indent_level -= 1
        self.write("</doStatement>")
        return
    
    def compile_return(self):
        self.write("<returnStatement>")
        self.indent_level += 1
        self.write(f"<keyword> {self.tokenizer.keyword()} </keyword>")  # 'return'
        self.tokenizer.advance()
        # If the next token is not the symbol ';', there is an expression to compile
        if not (self.tokenizer.token_type() == JackTokenizer.TokenType.SYMBOL and self.tokenizer.symbol() == ';'):
            self.compile_expression()
        self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # ';'
        self.tokenizer.advance()
        self.indent_level -= 1
        self.write("</returnStatement>")
        return
    
    def compile_expression(self):
        self.write("<expression>")
        self.indent_level += 1
        self.compile_term()
        while self.tokenizer.token_type() == JackTokenizer.TokenType.SYMBOL and self.tokenizer.symbol() in ('+', '-', '*', '/', '&', '|', '<', '>', '='):
            self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # op
            self.tokenizer.advance()
            self.compile_term()
        self.indent_level -= 1
        self.write("</expression>")
        return
    
    def compile_term(self):
        self.write("<term>")
        self.indent_level += 1
        token_type = self.tokenizer.token_type()
        
        if token_type == JackTokenizer.TokenType.INT_CONST:
            self.write(f"<integerConstant> {self.tokenizer.int_val()} </integerConstant>")
            self.tokenizer.advance()
        elif token_type == JackTokenizer.TokenType.STRING_CONST:
            self.write(f"<stringConstant> {self.tokenizer.string_val()} </stringConstant>")
            self.tokenizer.advance()
        elif token_type == JackTokenizer.TokenType.KEYWORD:
            self.write(f"<keyword> {self.tokenizer.keyword()} </keyword>")
            self.tokenizer.advance()
        elif token_type == JackTokenizer.TokenType.IDENTIFIER:
            self.write(f"<identifier> {self.tokenizer.identifier()} </identifier>")
            self.tokenizer.advance()
            if self.tokenizer.token_type() == JackTokenizer.TokenType.SYMBOL and self.tokenizer.symbol() == '[':
                self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # '['
                self.tokenizer.advance()
                self.compile_expression()
                self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # ']'
                self.tokenizer.advance()
            elif self.tokenizer.token_type() == JackTokenizer.TokenType.SYMBOL and self.tokenizer.symbol() in ('(', '.'):
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
        elif token_type == JackTokenizer.TokenType.SYMBOL and self.tokenizer.symbol() == '(':
            self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # '('
            self.tokenizer.advance()
            self.compile_expression()
            self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # ')'
            self.tokenizer.advance()
        elif token_type == JackTokenizer.TokenType.SYMBOL and self.tokenizer.symbol() in ('-', '~'):
            self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # unaryOp
            self.tokenizer.advance()
            self.compile_term()
        
        self.indent_level -= 1
        self.write("</term>")
        return
    
    def compile_expression_list(self):
        self.write("<expressionList>")
        self.indent_level += 1
        if self.tokenizer.token_type() != JackTokenizer.TokenType.SYMBOL or self.tokenizer.symbol() != ')':
            self.compile_expression()
            while self.tokenizer.token_type() == JackTokenizer.TokenType.SYMBOL and self.tokenizer.symbol() == ',':
                self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # ','
                self.tokenizer.advance()
                self.compile_expression()
        self.indent_level -= 1
        self.write("</expressionList>")
        return