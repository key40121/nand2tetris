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
        function_type = self.tokenizer.keyword()  # for symbol table and code generation
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
        numargs = self.compile_parameter_list(function_type)
        self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # ')'
        self.tokenizer.advance()
        numLocals = self.compile_subroutine_body(function_name, function_type, numargs)
        self.indent_level -= 1
        self.write("</subroutineDec>")

        print("subroutine class table")
        self.symbol_table_subroutine.show()  # for debugging

        return
    
    def compile_parameter_list(self, function_type):
        numArgs = 0
        if function_type == 'method':
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
    
    def compile_subroutine_body(self, function_name, function_type, numargs):
        self.write("<subroutineBody>")
        self.indent_level += 1
        self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # '{'
        self.tokenizer.advance()
        while self.tokenizer.token_type() == JackTokenizer.TokenType.KEYWORD and self.tokenizer.keyword() == 'var':
            self.compile_var_dec()
        self.vm_writer.writeFunction(f"{self.class_name}.{function_name}", self.symbol_table_subroutine.varCount('var'))
        if function_type == 'constructor':
            # for constructor, we need to push the base address of the new object onto the stack before returning
            self.vm_writer.writePush(VMWriter.Segment.CONSTANT, numargs)  # push base address of new object (which is now in pointer 0 after Memory.alloc)
            self.vm_writer.writeCall('Memory.alloc', 1)  # call Memory.alloc to allocate memory for the new object
        elif function_type == 'method':
            # for method, we need to push 'this' (the object reference) as the first argument before returning
            self.vm_writer.writePush(VMWriter.Segment.ARGUMENT, 0)  # push 'this' (the object reference) as the first argument for method call
            self.vm_writer.writePop(VMWriter.Segment.POINTER, 0)  # set 'this' pointer to the current object reference for method call
        self.compile_statements(isConstructor=(function_type == 'constructor'))
        self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # '}'
        self.tokenizer.advance()
        self.indent_level -= 1
        self.write("</subroutineBody>")
        return self.symbol_table_subroutine.varCount('var')
    
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
    
    def compile_statements(self, isConstructor=False):
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
                # if isConstructor:
                    # for constructor, we need to return the base address of the new object (which is now in pointer 0 after Memory.alloc)
                    # self.vm_writer.writePush(VMWriter.Segment.POINTER, 0)  # push base address of new object
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
        actual_index = self.symbol_table_subroutine.indexOf(varName)
        if actual_kind is None or actual_index is None:
            actual_kind = self.symbol_table_class.kindOf(varName)
            actual_index = self.symbol_table_class.indexOf(varName)
        if actual_kind == 'argument':
            segment = VMWriter.Segment.ARGUMENT
        elif actual_kind == 'var':
            segment = VMWriter.Segment.LOCAL
        elif actual_kind == 'static':
            segment = VMWriter.Segment.STATIC
        elif actual_kind == 'field':
            segment = VMWriter.Segment.THIS
        else:
            print(f"Undefined variable {varName} in let statement")  # for debugging
            raise Exception(f"Undefined variable {varName}")
        self.vm_writer.writePop(segment, actual_index)  # for VM code generation
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
        label_id = self.label_count  # for unique labels in if statements
        self.vm_writer.writeArithmetic(VMWriter.Command.NOT)  # if-goto expects true condition, so negate the expression result
        self.vm_writer.writeIf(f"IF_FALSE{label_id}")  # label for if false
        self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # ')'
        self.tokenizer.advance()
        self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # '{'
        self.tokenizer.advance()
        self.compile_statements()
        self.vm_writer.writeGoto(f"IF_END{label_id}")  # label for if end
        self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # '}'
        self.tokenizer.advance()

        # optional else clause
        if self.tokenizer.token_type() == JackTokenizer.TokenType.KEYWORD and self.tokenizer.keyword() == 'else':
            self.write(f"<keyword> {self.tokenizer.keyword()} </keyword>")  # 'else'
            self.tokenizer.advance()
            self.vm_writer.writeLabel(f"IF_FALSE{label_id}")  # label for else clause
            self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # '{'
            self.tokenizer.advance()
            self.compile_statements()
            self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # '}'
            self.tokenizer.advance()

        self.vm_writer.writeLabel(f"IF_END{label_id}")  # label for if end
        self.indent_level -= 1
        self.write("</ifStatement>")
        return
    
    def compile_while(self):
        self.write("<whileStatement>")
        self.indent_level += 1
        self.write(f"<keyword> {self.tokenizer.keyword()} </keyword>")  # 'while'
        self.tokenizer.advance()
        self.label_count += 1
        writeIndex = self.label_count  # for unique labels in while statements
        self.vm_writer.writeLabel(f"WHILE_EXP{writeIndex}")  # label for while expression
        self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # '('
        self.tokenizer.advance()
        self.compile_expression()
        self.vm_writer.writeArithmetic(VMWriter.Command.NOT)  # if-goto expects true condition, so negate the expression result
        self.label_count += 1
        whileFinishLabel = f"WHILE_END{self.label_count}"
        self.vm_writer.writeIf(f"WHILE_END{self.label_count}")  # label for while end
        self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # ')'
        self.tokenizer.advance()
        self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  #
        self.tokenizer.advance()
        self.compile_statements()
        self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # '}'
        self.tokenizer.advance()
        self.indent_level -= 1
        self.write("</whileStatement>")
        self.vm_writer.writeGoto(f"WHILE_EXP{writeIndex}")  # go back to while expression
        self.vm_writer.writeLabel(f"{whileFinishLabel}")  # label for while expression
        return
  
    def compile_do(self):
        self.write("<doStatement>")
        self.indent_level += 1
        self.write(f"<keyword> {self.tokenizer.keyword()} </keyword>")  # 'do'
        self.tokenizer.advance()
        self.write(f"<identifier> {self.tokenizer.identifier()} </identifier>")  # subroutineName or className or varName
        name = self.tokenizer.identifier()  # for VM code generation
        subroutine_name = None  # for VM code generation

        method_object = self.symbol_table_subroutine.kindOf(name)  # check if it's a method call on a variable
        if method_object is not None:
            print(f"do statement: found method call on variable {name} of kind {method_object}")  # for debugging
            # It's a method call on a variable, so we need to push the variable as the first argument
            if method_object == 'var':
                segment = VMWriter.Segment.LOCAL
            elif method_object == 'argument':
                segment = VMWriter.Segment.ARGUMENT
            elif method_object == 'static':
                segment = VMWriter.Segment.STATIC
            elif method_object == 'field':
                segment = VMWriter.Segment.THIS
            else:
                raise Exception(f"Undefined variable: {name}")
            self.vm_writer.writePush(segment, self.symbol_table_subroutine.indexOf(name))  # push the object reference as the first argument

        isClassMethodCall = False

        self.tokenizer.advance()
        if self.tokenizer.token_type() == JackTokenizer.TokenType.SYMBOL and self.tokenizer.symbol() == '.':
            self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # '.'
            self.tokenizer.advance()
            self.write(f"<identifier> {self.tokenizer.identifier()} </identifier>")  # subroutineName
            subroutine_name = self.tokenizer.identifier()  # for VM code generation
            self.tokenizer.advance()
        else:
            isClassMethodCall = True
        self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # '('
        self.tokenizer.advance()
        numargs = self.compile_expression_list()
        self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # ')'
        self.tokenizer.advance()  # consume ')'
        self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # ';'
        self.tokenizer.advance()  # consume ';'
        self.indent_level -= 1
        self.write("</doStatement>")

        if isClassMethodCall:
            self.vm_writer.writeCall(f"{self.class_name}.{name}", numargs + 1)  # class method call, so use name as class name
            self.vm_writer.writePop(VMWriter.Segment.TEMP, 0)  # discard return value of do statement
            return

        method_type = self.symbol_table_subroutine.typeOf(name)  # check if it's a method call on a variable again for VM code generation
        if method_type is None:
            method_type = self.symbol_table_class.typeOf(name)


        if method_type is not None:
            full_call_name = f"{method_type}.{subroutine_name}"  # method call on a variable, so use the variable's type as the class name
            numargs += 1  # for method calls on variables, we need to add 1 to the number of arguments to account for the object reference
        else:
            full_call_name = f"{name}.{subroutine_name}"  # not a method call on a variable, so use the name as the class name

        self.vm_writer.writeCall(full_call_name, numargs)  # for VM code generation
        self.vm_writer.writePop(VMWriter.Segment.TEMP, 0)  # discard return value of do statement
        return
    
    def compile_return(self):
        self.write("<returnStatement>")
        self.indent_level += 1
        self.write(f"<keyword> {self.tokenizer.keyword()} </keyword>")  # 'return'
        self.tokenizer.advance()
        is_void = True  # assume void return until we see an expression
        # If the next token is not the symbol ';', there is an expression to compile
        if not (self.tokenizer.token_type() == JackTokenizer.TokenType.SYMBOL and self.tokenizer.symbol() == ';'):
            self.compile_expression()
            is_void = False
        self.write(f"<symbol> {self.tokenizer.symbol()} </symbol>")  # ';'
        self.tokenizer.advance()
        self.indent_level -= 1
        if is_void == True:
            self.vm_writer.writePush(VMWriter.Segment.CONSTANT, 0)  # push dummy value for void return  
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
            if self.tokenizer.keyword() in ['true', 'false', 'null', 'this']:
                    # for VM code generation, we can push the keyword constant and let the VM handle it
                if self.tokenizer.keyword() == 'true':
                    self.vm_writer.writePush(VMWriter.Segment.CONSTANT, 0)  # true is represented as -1 in VM, but we can push 1 and let the VM handle it
                    self.vm_writer.writeArithmetic(VMWriter.Command.NOT)  # negate 1 to get -1 for true
                elif self.tokenizer.keyword() == 'this':
                    self.vm_writer.writePush(VMWriter.Segment.POINTER, 0)  # push 'this' reference for VM code generation
                else:
                    self.vm_writer.writePush(VMWriter.Segment.CONSTANT, 0)  # false and null are represented as 0 in VM
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
                if kind is None:
                    kind = self.symbol_table_class.kindOf(identifier_name)
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
                identifier_index = self.symbol_table_subroutine.indexOf(identifier_name) if self.symbol_table_subroutine.indexOf(identifier_name) is not None else self.symbol_table_class.indexOf(identifier_name)
                self.vm_writer.writePush(segment, identifier_index)
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