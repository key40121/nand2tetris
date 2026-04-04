import sys
import JackTokenizer
import SymbolTable
import VMWriter

class CompilationEngine:
    def __init__(self, tokenizer, output_stream):
        self.tokenizer = tokenizer
        self.output_stream = output_stream
        self.vm_writer = VMWriter.VMWriter(output_stream)
        self.symbol_table_class = SymbolTable.SymbolTable()
        self.symbol_table_subroutine = SymbolTable.SymbolTable()
        self.indent_level = 0
        self.class_name = None  # to keep track of the current class name for symbol table and code generation
        self.label_count = 0  # for generating unique labels in if and while statements

    def write(self, content):
        indent = '  ' * self.indent_level
        # self.output_stream.write(f"{indent}{content}\n")

    def compile_class(self):
        self.symbol_table_class.reset()
        self.symbol_table_subroutine.reset()
        self.write("<class>")
        self.indent_level += 1

        self.write(f"<keyword> {self.tokenizer.keyword()} </keyword>")  # 'class'
        self.tokenizer.advance()
        self.write(f"<identifier> {self.tokenizer.identifier()} </identifier>")  # class name
        self.class_name = self.tokenizer.identifier()  # for symbol table and code generation
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

        print("class symbol table")
        self.symbol_table_class.show()  # for debugging
        self.write("</class>")
      
    def compile_class_var_dec(self):
        # static or field
        name = []
        self.write(f"<classVarDec>")
        self.indent_level += 1
        self.write(f"<keyword> {self.tokenizer.keyword()} </keyword>")  # 'static' or 'field'
        kind = self.tokenizer.keyword()  # for symbol table
        self.tokenizer.advance()
        if self.tokenizer.token_type() == JackTokenizer.TokenType.KEYWORD:
            self.write(f"<keyword> {self.tokenizer.keyword()} </keyword>")  # type
            type = self.tokenizer.keyword()  # for symbol table
        else:
            self.write(f"<identifier> {self.tokenizer.identifier()} </identifier>")  # type (class name)
            type = self.tokenizer.identifier()  # for symbol table
        self.tokenizer.advance()
        self.write(f"<identifier> {self.tokenizer.identifier()} </identifier>")  # varName
        name.append(self.tokenizer.identifier())  # for symbol table
        self.tokenizer.advance()
        self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # ',' or ';'
        while self.tokenizer.symbol() == ',':
            self.tokenizer.advance()
            self.write(f"<identifier> {self.tokenizer.identifier()} </identifier>")  # varName
            name.append(self.tokenizer.identifier())  # for symbol table
            self.tokenizer.advance()
            self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # ',' or ';'
        self.tokenizer.advance()  # skip ';'
        self.indent_level -= 1
        self.write(f"</classVarDec>")

        # for symbol table
        for (name) in name:
            self.symbol_table_class.define(name, type, kind)
        return
    
    def compile_subroutine(self):
        self.symbol_table_subroutine.reset()
        # constructor, function, or method

        function_name = None  # for VM code generation
        function_return_type = None  # for VM code generation

        self.write("<subroutineDec>")
        self.indent_level += 1
        self.write(f"<keyword> {self.tokenizer.keyword()} </keyword>")  # 'constructor'/'function'/'method'
        self.tokenizer.advance()
        # Return type can be keyword (void, int, boolean) or identifier (class name)
        if self.tokenizer.token_type() == JackTokenizer.TokenType.KEYWORD:
            self.write(f"<keyword> {self.tokenizer.keyword()} </keyword>")  # 'void' or type
            function_return_type = self.tokenizer.keyword() # for VM code generation
        else:
            self.write(f"<identifier> {self.tokenizer.identifier()} </identifier>")  # type (class name)
            function_return_type = self.tokenizer.identifier()  # for VM code generation
        self.tokenizer.advance()
        self.write(f"<identifier> {self.tokenizer.identifier()} </identifier>")  # subroutineName
        function_name = self.tokenizer.identifier()
        self.tokenizer.advance()
        self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # '('
        self.tokenizer.advance()
        numargs = self.compile_parameter_list()
         # for VM code generation, we need to know the number of local variables
        # which we can get from the symbol table after compiling the subroutine body
        self.vm_writer.writeFunction(f"{self.class_name}.{function_name}", numargs) # subtract 1 for 'this' argument
        self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # ')'
        self.tokenizer.advance()
        self.compile_subroutine_body()
        self.indent_level -= 1
        self.write("</subroutineDec>")

        print("subroutine class table")
        self.symbol_table_subroutine.show()  # for debugging

        if function_return_type == 'void':
            self.vm_writer.writePush(VMWriter.Segment.CONSTANT, 0)  # push dummy value for void return
            self.vm_writer.writeReturn()
        return
    
    def compile_parameter_list(self):
        numArgs = 0
        self.symbol_table_subroutine.define("this", self.class_name, 'argument')  # for methods, 'this' is the first argument
        self.write("<parameterList>")
        self.indent_level += 1
        if self.tokenizer.token_type() in [JackTokenizer.TokenType.KEYWORD, JackTokenizer.TokenType.IDENTIFIER]:
            self.write(f"<keyword> {self.tokenizer.keyword()} </keyword>")  # type
            self.tokenizer.advance()
            type = self.tokenizer.keyword()
            self.write(f"<identifier> {self.tokenizer.identifier()} </identifier>")  # varName
            varName = self.tokenizer.identifier()
            self.symbol_table_subroutine.define(varName, type, 'argument')  # for symbol table
            numArgs += 1
            self.tokenizer.advance()
            while self.tokenizer.symbol() == ',':
                numArgs += 1
                self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # ','
                self.tokenizer.advance()
                self.write(f"<keyword> {self.tokenizer.keyword()} </keyword>")  # type
                self.tokenizer.advance()
                type = self.tokenizer.keyword()
                self.write(f"<identifier> {self.tokenizer.identifier()} </identifier>")  # varName
                varName = self.tokenizer.identifier()
                self.symbol_table_subroutine.define(varName, type, 'argument')  # for symbol table
                self.tokenizer.advance()
        self.indent_level -= 1
        self.write("</parameterList>")
        return numArgs
    
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
            type = self.tokenizer.keyword()  # for symbol table
        else:
            self.write(f"<identifier> {self.tokenizer.identifier()} </identifier>")  # type (class name)
            type = self.tokenizer.identifier()  # for symbol table
        name = []
        self.tokenizer.advance()
        self.write(f"<identifier> {self.tokenizer.identifier()} </identifier>")  # varName
        name.append(self.tokenizer.identifier())  # for symbol table
        self.tokenizer.advance()
        self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # ',' or ';'
        while self.tokenizer.symbol() == ',':
            self.tokenizer.advance()
            self.write(f"<identifier> {self.tokenizer.identifier()} </identifier>")  # varName
            name.append(self.tokenizer.identifier())  # for symbol table
            self.tokenizer.advance()
            self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # ',' or ';'
        self.tokenizer.advance()  # skip ';'
        self.indent_level -= 1
        self.write(f"</varDec>")
        # for symbol table
        for (name) in name:
            self.symbol_table_subroutine.define(name, type, 'var')
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
        varName = self.tokenizer.identifier()  # for VM code generation
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
        actual_kind = self.symbol_table_subroutine.kindOf(varName)
        if actual_kind == 'argument':
            segment = VMWriter.Segment.ARGUMENT
        elif actual_kind == 'var':
            segment = VMWriter.Segment.LOCAL
        elif actual_kind == 'static':
            segment = VMWriter.Segment.STATIC
        elif actual_kind == 'field':
            segment = VMWriter.Segment.THIS
        else:
            raise Exception(f"Undefined variable {varName}")
        self.vm_writer.writePop(segment, self.symbol_table_subroutine.indexOf(varName))
        print(f"let statement: pop {segment} {self.symbol_table_subroutine.indexOf(varName)}")  # for debugging
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
        self.label_count += 1
        self.vm_writer.writeArithmetic(VMWriter.Command.NOT)  # if-goto expects true condition, so negate the expression result
        self.vm_writer.writeIf(f"IF_FALSE{self.label_count}")
        self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # ')'
        self.tokenizer.advance()
        self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # '{'
        self.tokenizer.advance()
        self.compile_statements()
        self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # '}'
        self.tokenizer.advance()

        # optional else clause
        if self.tokenizer.token_type() == JackTokenizer.TokenType.KEYWORD and self.tokenizer.keyword() == 'else':
            self.write(f"<keyword> {self.tokenizer.keyword()} </keyword>")  # 'else'
            self.tokenizer.advance()
            self.vm_writer.writeLabel(f"IF_FALSE{self.label_count}")  # label for else clause
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
        name = self.tokenizer.identifier()  # for VM code generation
        subroutine_name = None  # for VM code generation
        self.tokenizer.advance()
        if self.tokenizer.token_type() == JackTokenizer.TokenType.SYMBOL and self.tokenizer.symbol() == '.':
            self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # '.'
            self.tokenizer.advance()
            self.write(f"<identifier> {self.tokenizer.identifier()} </identifier>")  # subroutineName
            subroutine_name = self.tokenizer.identifier()  # for VM code generation
            self.tokenizer.advance()
        self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # '('
        self.tokenizer.advance()
        numargs = self.compile_expression_list()
        self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # ')'
        self.tokenizer.advance()  # consume ')'
        self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # ';'
        self.tokenizer.advance()  # consume ';'
        self.indent_level -= 1
        self.write("</doStatement>")

        self.vm_writer.writeCall(f"{name}.{subroutine_name}", numargs)  # for VM code generation
        self.vm_writer.writePop(VMWriter.Segment.TEMP, 0)  # discard return value of do statement
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
        self.vm_writer.writeReturn()  # for VM code generation
        self.write("</returnStatement>")
        return
    
    def compile_expression(self):
        self.write("<expression>")
        self.indent_level += 1
        self.compile_term()
        op = []
        while self.tokenizer.token_type() == JackTokenizer.TokenType.SYMBOL and self.tokenizer.symbol() in ('+', '-', '*', '/', '&', '|', '<', '>', '='):
            if self.tokenizer.symbol() == '<':
                self.write(f"<symbol> &lt; </symbol>")  # op
            elif self.tokenizer.symbol() == '>':
                self.write(f"<symbol> &gt; </symbol>")  # op
            elif self.tokenizer.symbol() == '&':
                self.write(f"<symbol> &amp; </symbol>")  # op
            else:
                self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # op
            op.append(self.tokenizer.symbol())  # for VM code generation
            self.tokenizer.advance()
            self.compile_term()
            for (op) in op:
                if op == '+':
                    self.vm_writer.writeArithmetic(VMWriter.Command.ADD)
                elif op == '-':
                    self.vm_writer.writeArithmetic(VMWriter.Command.SUB)
                elif op == '*':
                    self.vm_writer.writeCall('Math.multiply', 2)
                elif op == '/':
                    self.vm_writer.writeCall('Math.divide', 2)
                elif op == '&':
                    self.vm_writer.writeArithmetic(VMWriter.Command.AND)
                elif op == '|':
                    self.vm_writer.writeArithmetic(VMWriter.Command.OR)
                elif op == '<':
                    self.vm_writer.writeArithmetic(VMWriter.Command.LT)
                elif op == '>':
                    self.vm_writer.writeArithmetic(VMWriter.Command.GT)
                elif op == '=':
                    self.vm_writer.writeArithmetic(VMWriter.Command.EQ)
        self.indent_level -= 1
        self.write("</expression>")
        return
    
    def compile_term(self):
        self.write("<term>")
        self.indent_level += 1
        token_type = self.tokenizer.token_type()
        
        if token_type == JackTokenizer.TokenType.INT_CONST:
            self.write(f"<integerConstant> {self.tokenizer.int_val()} </integerConstant>")
            self.vm_writer.writePush(VMWriter.Segment.CONSTANT, self.tokenizer.int_val())
            self.tokenizer.advance()
        elif token_type == JackTokenizer.TokenType.STRING_CONST:
            self.write(f"<stringConstant> {self.tokenizer.string_val()} </stringConstant>")
            self.vm_writer.writePush(VMWriter.Segment.CONSTANT, self.tokenizer.string_val())
            self.tokenizer.advance()
        elif token_type == JackTokenizer.TokenType.KEYWORD:
            self.write(f"<keyword> {self.tokenizer.keyword()} </keyword>")
            self.tokenizer.advance()
        elif token_type == JackTokenizer.TokenType.IDENTIFIER:
            self.write(f"<identifier> {self.tokenizer.identifier()} </identifier>")
            identifier_name = self.tokenizer.identifier()  #
            self.tokenizer.advance()
            if self.tokenizer.token_type() == JackTokenizer.TokenType.SYMBOL and self.tokenizer.symbol() == '[':
                self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # '['
                self.tokenizer.advance()
                self.compile_expression()
                self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # ']'
                self.tokenizer.advance()
            elif self.tokenizer.token_type() == JackTokenizer.TokenType.SYMBOL and self.tokenizer.symbol() in ('(', '.'):
                # subroutine call
                subroutine_name = None  # Initialize for local method calls
                if self.tokenizer.symbol() == '.':
                    self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # '.'
                    self.tokenizer.advance()
                    self.write(f"<identifier> {self.tokenizer.identifier()} </identifier>")  # subroutineName
                    subroutine_name = self.tokenizer.identifier()  # for VM code generation
                    self.tokenizer.advance()
                self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # '('
                self.tokenizer.advance()
                numArgs = self.compile_expression_list()
                full_call_name = f"{identifier_name}.{subroutine_name}" if subroutine_name else identifier_name
                self.vm_writer.writeCall(full_call_name, numArgs)
                self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # ')'
                self.tokenizer.advance()
            else:
                # Variable reference - convert symbol table kind to VM segment
                kind = self.symbol_table_subroutine.kindOf(identifier_name)
                if kind == 'var':
                    segment = VMWriter.Segment.LOCAL
                elif kind == 'argument':
                    segment = VMWriter.Segment.ARGUMENT
                elif kind == 'static':
                    segment = VMWriter.Segment.STATIC
                elif kind == 'field':
                    segment = VMWriter.Segment.THIS
                else:
                    raise Exception(f"Undefined variable: {identifier_name}")
                self.vm_writer.writePush(segment, self.symbol_table_subroutine.indexOf(identifier_name))
        elif token_type == JackTokenizer.TokenType.SYMBOL and self.tokenizer.symbol() == '(':
            self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # '('
            self.tokenizer.advance()
            self.compile_expression()
            self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # ')'
            self.tokenizer.advance()
        elif token_type == JackTokenizer.TokenType.SYMBOL and self.tokenizer.symbol() in ('-', '~'):
            self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # unaryOp
            negExpression = self.tokenizer.symbol()  # for VM code generation
             # for VM code generation, we need to compile the term first before writing the unary command
            self.tokenizer.advance()
            self.compile_term()

            self.vm_writer.writeArithmetic(VMWriter.Command.NEG if negExpression == '-' else VMWriter.Command.NOT)  # for VM code generation
        
        self.indent_level -= 1
        self.write("</term>")
        return
    
    def compile_expression_list(self):
        numargs = 0
        self.write("<expressionList>")
        self.indent_level += 1
        if self.tokenizer.token_type() != JackTokenizer.TokenType.SYMBOL or self.tokenizer.symbol() != ')':
            self.compile_expression()
            numargs += 1
            while self.tokenizer.token_type() == JackTokenizer.TokenType.SYMBOL and self.tokenizer.symbol() == ',':
                self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # ','
                self.tokenizer.advance()
                self.compile_expression()
                numargs += 1
        self.indent_level -= 1
        self.write("</expressionList>")
        return numargs