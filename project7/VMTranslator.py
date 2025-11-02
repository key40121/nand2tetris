from enum import Enum
import sys

class CommandType(Enum):
  C_ARITHMETIC = 1
  C_PUSH = 2
  C_POP = 3
  C_LABEL = 4
  C_GOTO = 5
  C_IF = 6
  C_FUNCTION = 7
  C_RETURN = 8
  C_CALL = 9

class Parser:
  def __init__(self, file_name, encoding='utf-8'):
    """
    This class handles the input file.
    - Handles the parsing of a single .vm file,
    - Reads a VM command, parses it, and provides convenient access to the command's components.
    - Ignores all white space and comments.
    """
    self.file = open(file_name, 'r', encoding=encoding)
    self.line = None

  def advance(self):
    """this function returns current line, actually not advancing..."""
    return

  def hasMoreLines(self) -> bool:
    """
    if true, a new line is set to self.line.
    if false, there is no more line in the file.
    """
    while True:
      line = self.file.readline()
      if not line: # EOF
        return False
      # Remove comments and whitespace
      stripped_line = line.split("//", 1)[0].strip()
      if stripped_line == "":
        continue
      self.line = stripped_line
      return True

  def commandType(self) -> CommandType:
    """
    Call after check hasMoreLines == true
    Retuns a constant representing the type of the current command.
    """
    if self.line.startswith("eq") or self.line.startswith("add") or self.line.startswith("sub"):
      return CommandType.C_ARITHMETIC
    elif self.line.startswith("push"):
      return CommandType.C_PUSH
    elif self.line.startswith('pop'):
      return CommandType.C_POP
    elif self.line.startswith("label"):
      return CommandType.C_LABEL
    elif self.line.startswith("goto"):
      return CommandType.C_GOTO
    elif self.line.startswith("if-goto"):
      return CommandType.C_IF
    elif self.line.startswith("function"):
      return CommandType.C_FUNCTION
    elif self.line.startswith("call"):
      return CommandType.C_CALL
    elif self.line.startswith("return"):
      return CommandType.C_RETURN

  def arg1(self):
    """
    Returns the first argument of the current command.
    If the current command is C_ARITHMETIC, the command itself (add, sub, etc.) is returned.
    Called only if the current command is not C_RETURN.
    """

    divided_line = self.line.split()
    if self.commandType() == CommandType.C_ARITHMETIC:
      return divided_line[0]
    return divided_line[1]
  
  def arg2(self):
    """
    Returns the second argument of the current command.
    Called only if the current command is C_PUSH, C_POP, C_FUNCTION, or C_CALL.
    """
    if self.commandType() in (CommandType.C_PUSH, CommandType.C_POP, CommandType.C_FUNCTION, CommandType.C_CALL):
      divided_line = self.line.split()
      return int(divided_line[2])

    if self.commandType() not in (CommandType.C_PUSH, CommandType.C_POP, CommandType.C_FUNCTION, CommandType.C_CALL):
      print("Error: arg2 called on invalid command type")
      return


class CodeWriter:
  def __init__(self, file_name=None):
    """
    This class handles the output file
    """
    self.file = None
    if file_name:
      self.file = open(file_name + '.asm', 'w', encoding='utf-8')
    
  def writeArithmetic(self, command):
    """
    Writes to the output file the assembly code that implements the given arithmetic-logical command.
    """
    if command not in ['add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not']:
      print("Error: Invalid command for writeArithmetic:", command)
      return

    if command == 'add':
      self.file.write("// add\n")
      self.file.write("// SP--\n")
      self.file.write("@SP\n")
      self.file.write("M=M-1\n")
      self.file.write("A=M\n")
      self.file.write("D=M\n")  # D = *SP

      self.file.write("// R13 = *SP - 1\n ")
      self.file.write("@R13\n")
      self.file.write("M=D\n")  # R13 = *SP

      self.file.write("// SP--\n")
      self.file.write("@SP\n")
      self.file.write("M=M-1\n")
      self.file.write("A=M\n")
      
      self.file.write("// D = *SP + R13\n")
      self.file.write("D=M+D\n")
      self.file.write("// RAM[SP] = D\n")
      self.file.write("@SP\n")
      self.file.write("A=M\n")
      self.file.write("M=D\n")
      self.file.write("// SP++\n")
      self.file.write("@SP\n")
      self.file.write("M=M+1\n")
      return
    
    elif command == 'sub':
      self.file.write("// sub\n")
      self.file.write("// SP--\n")
      self.file.write("@SP\n")
      self.file.write("M=M-1\n")
      self.file.write("A=M\n")
      self.file.write("D=M\n")  # D = *SP

      self.file.write("// R13 = *SP - 1\n ")
      self.file.write("@R13\n")
      self.file.write("M=D\n")  # R13 = *SP

      self.file.write("// SP--\n")
      self.file.write("@SP\n")
      self.file.write("M=M-1\n")
      self.file.write("A=M\n")

      self.file.write("// D = *SP - R13\n")
      self.file.write("D=M-D\n")
      self.file.write("// RAM[SP] = D\n")
      self.file.write("@SP\n")
      self.file.write("A=M\n")
      self.file.write("M=D\n")
      self.file.write("// SP++\n")
      self.file.write("@SP\n")
      self.file.write("M=M+1\n")
      return

    elif command == 'neg':
      self.file.write("// neg\n")
      self.file.write("// SP--\n")
      self.file.write("@SP\n")
      self.file.write("M=M-1\n")
      self.file.write("A=M\n")
      self.file.write("M=-M\n")  # *SP = -(*SP)
      self.file.write("// SP++\n")
      self.file.write("@SP\n")
      self.file.write("M=M+1\n")
      return
    
    elif command == 'eq':
      #implement true as -1 and false as 0
      self.file.write("// eq\n")
      # pop y into D
      self.file.write("// SP--\n")
      self.file.write("@SP\n")
      self.file.write("M=M-1\n")
      self.file.write("A=M\n")
      self.file.write("D=M\n")

      # pop x and compute D = x -y
      self.file.write("// SP-- ; D = x - y\n")
      self.file.write("@SP\n")
      self.file.write("AM=M-1\n")
      self.file.write("D=M-D\n")  # D = x - y

      # unique labels
      true_label = f"EQ_TRUE{self.label_counter}"
      end_label = f"EQ_END{self.label_counter}"
      self.label_counter += 1

      # Branching here
      self.file.write("// if D==0 jump to TRUE\n")
      self.file.write(f"@{true_label}\n")
      self.file.write("D;JEQ\n")

      # false case: set D=0 (false)
      self.file.write("// false case: set D=0 (false)\n")
      self.file.write(f"({end_label})\n")
      self.file.write("@SP\n")
      self.file.write("A=M\n")
      self.file.write("M=0\n")
      self.file.write("// jump to END\n")
      self.file.write(f"@{end_label}\n")
      self.file.write("0;JMP\n")

      # true case: set D=-1 (true)
      self.file.write("// true case: set D=-1 (true)\n")
      self.file.write(f"({true_label})\n")
      self.file.write("@SP\n")
      self.file.write("A=M\n")
      self.file.write("M=-1\n")

      # jump to END
      self.file.write("// jump to END\n")
      self.file.write(f"({end_label})\n")

      # SP++
      self.file.write("// SP++\n")
      self.file.write("@SP\n")
      self.file.write("M=M+1\n")
      return
    
    elif command == 'gt':
      self.file.write("// gt\n")
      
      self.file.write("// SP--\n")
      self.file.write("@SP\n")
      self.file.write("M=M-1\n")
      self.file.write("A=M\n")
      self.file.write("D=M\n")  # D = *SP

      # pop y into D
      self.file.write("// R13 = *SP - 1\n ")
      self.file.write("@R13\n")
      self.file.write("M=D\n")  # R13 = *SP

      self.file.write("// SP--\n")
      self.file.write("@SP\n")
      self.file.write("M=M-1\n")
      self.file.write("A=M\n")
      
      # if x > y, D = x - y > 0
      self.file.write("// D = *SP - R13\n")
      self.file.write("D=M-D\n")

      # unique labels
      true_label = f"GT_TRUE{self.label_counter}"
      end_label = f"GT_END{self.label_counter}"
      self.label_counter += 1

      # Branching here
      self.file.write("// if D>0 jump to TRUE\n")
      self.file.write(f"@{true_label}\n")
      self.file.write("D;JGT\n")

      # false case: set D=0 (false)
      self.file.write("// false case: set D=0 (false)\n")
      self.file.write(f"({end_label})\n")
      self.file.write("@SP\n")
      self.file.write("A=M\n")
      self.file.write("M=0\n")
      self.file.write("// jump to END\n")
      self.file.write(f"@{end_label}\n")
      self.file.write("0;JMP\n")
      # true case: set D=-1 (true)
      self.file.write("// true case: set D=-1 (true)\n")
      self.file.write(f"({true_label})\n")
      self.file.write("@SP\n")
      self.file.write("A=M\n")
      self.file.write("M=-1\n")
      # jump to END
      self.file.write("// jump to END\n")
      self.file.write(f"({end_label})\n")

      # SP++
      self.file.write("// SP++\n")
      self.file.write("@SP\n")
      self.file.write("M=M+1\n")
      return
    
    elif command == 'lt':
      # To be implemented
      return
    
    elif command == 'and':
      # To be implemented
      return
    
    elif command == 'or':
      # To be implemented
      return  
    elif command == 'not':

      # To be implemented
      return

  def writePushPop(self, commandType, segment, index):
    """
    Writes to the output file the assembly code that implements the given push or pop command.
    """
    if commandType not in ['C_PUSH', 'C_POP']:
      print("Error: Invalid command for writePushPop:", commandType)
      return
    
    if commandType == 'C_PUSH':
      self.file.write(f"// push {segment} {index}\n")

      if segment == 'constant':
        self.file.write(f"// D = {index}\n")
        self.file.write(f"@{index}")
        self.file.write("\nD=A\n")

        self.file.write("// RAM[SP] = D\n")
        self.file.write("@SP\n")
        self.file.write("A=M\n")
        self.file.write("M=D\n")
        
        self.file.write("// SP++\n")
        self.file.write("@SP\n")
        self.file.write("M=M+1\n")
        return
      
      elif segment == 'temp':
        base_addr = 5
        self.file.write(f"// D = RAM[{base_addr + index}]\n")
        self.file.write(f"@{base_addr + index}\n")
        self.file.write("D=M\n")
        self.file.write("// RAM[SP] = D\n")
        self.file.write("@SP\n")
        self.file.write("A=M\n")
        self.file.write("M=D\n")
        self.file.write("// SP++\n")
        self.file.write("@SP\n")
        self.file.write("M=M+1\n")
        return
      
      elif segment == 'static':
        base_addr = 16
        self.file.write(f"// D = RAM[{base_addr + index}]\n")
        self.file.write(f"@{base_addr + index}\n")
        self.file.write("D=M\n")
        self.file.write("// RAM[SP] = D\n")
        self.file.write("@SP\n")
        self.file.write("A=M\n")
        self.file.write("M=D\n")
        self.file.write("// SP++\n")
        self.file.write("@SP\n")
        self.file.write("M=M+1\n")
        return
      
      elif segment == 'pointer':
        if index == 0:
          addr = "THIS"
        elif index == 1:
          addr = "THAT"
        else:
          print("Error: Invalid index for pointer segment in push:", index)
          return
        self.file.write(f"// D = RAM[{addr}]\n")
        self.file.write(f"@{addr}\n")
        self.file.write("D=M\n")
        self.file.write("// RAM[SP] = D\n")
        self.file.write("@SP\n")
        self.file.write("A=M\n")
        self.file.write("M=D\n")
        self.file.write("// SP++\n")
        self.file.write("@SP\n")
        self.file.write("M=M+1\n")
        return

      elif segment == 'local':
        addr = "LCL"
      elif segment == 'argument':
        addr = "ARG"
      elif segment == 'this':
        addr = "THIS"
      elif segment == 'that':
        addr = "THAT"

      self.file.write(f"// D = RAM[{addr}]\n")
      self.file.write(f"@{addr}\n")
      self.file.write("D=M\n")
      self.file.write(f"// A = D + {index}\n")
      self.file.write(f"@{index}\n")
      self.file.write("A=D+A\n")
      self.file.write(f"// D = RAM[{addr}] + {index}\n")
      self.file.write("D=M\n")
      self.file.write("// RAM[SP] = D\n")
      self.file.write("@SP\n")
      self.file.write("A=M\n")
      self.file.write("M=D\n")
      self.file.write("// SP++\n")
      self.file.write("@SP\n")
      self.file.write("M=M+1\n")
      return

      """
      -----------------------POP-----------------------
      """
    elif commandType == 'C_POP':
      self.file.write(f"// pop {segment} {index}\n")
      if segment == 'temp':
        base_addr = 5
        self.file.write(f"// SP--\n")
        self.file.write("@SP\n")
        self.file.write("AM=M-1\n")
        self.file.write("D=M\n")  # D = *SP
        self.file.write(f"// RAM[{base_addr + index}] = RAM[SP]\n")
        self.file.write(f"@{base_addr + index}\n")
        self.file.write("M=D\n")
        return
      
      elif segment == 'static':
        base_addr = 16
        self.file.write(f"// SP--\n")
        self.file.write("@SP\n")
        self.file.write("AM=M-1\n")
        self.file.write("D=M\n")  # D = *SP
        self.file.write(f"// RAM[{base_addr + index}] = RAM[SP]\n")
        self.file.write(f"@{base_addr + index}\n")
        self.file.write("M=D\n")
        return
      
      elif segment == 'pointer':
        if index == 0:
          addr = "THIS"
        elif index == 1:
          addr = "THAT"
        else:
          print("Error: Invalid index for pointer segment in pop:", index)
          return
        self.file.write(f"// SP--\n")
        self.file.write("@SP\n")
        self.file.write("AM=M-1\n")
        self.file.write("D=M\n")  # D = *SP
        self.file.write(f"// RAM[{addr}] = RAM[SP]\n")
        self.file.write(f"@{addr}\n")
        self.file.write("M=D\n")
        return
      
      elif segment == 'local':
        addr = "LCL"
      elif segment == 'argument':
        addr = "ARG"
      elif segment == 'this':
        addr = "THIS"
      elif segment == 'that':
        addr = "THAT"
      
      self.file.write(f"// Compute address RAM[{addr}] + {index} and store in R13\n")
      self.file.write(f"@{addr}\n")
      self.file.write("D=M\n")
      self.file.write(f"@{index}\n")
      self.file.write("D=D+A\n")
      self.file.write("@R13\n")  # Use R13 as a temp storage
      self.file.write("M=D\n")
      self.file.write(f"// SP--\n")
      self.file.write("@SP\n")
      self.file.write("AM=M-1\n")
      self.file.write("D=M\n")  # D = *SP
      self.file.write(f"// RAM[add] = RAM[SP]\n")
      self.file.write("@R13\n")
      self.file.write("A=M\n")
      self.file.write("M=D\n")
      return

  def close(self):
    """Closes the output file."""
    if self.file:
      self.file.close()

class VMTranslator:
  def __init__(self, file_name):
    self.file_name = file_name
    self.parser = Parser(file_name)
    self.code_writer = CodeWriter()

  def start(self):
    while self.parser.hasMoreLines():
      command_type = self.parser.commandType()
      if command_type == CommandType.C_ARITHMETIC:
        command = self.parser.arg1()
        self.code_writer.writeArithmetic(command)
      elif command_type in (CommandType.C_PUSH, CommandType.C_POP):
        segment = self.parser.arg1()
        index = self.parser.arg2()
        self.code_writer.writePushPop(command_type.name, segment, index)
    self.code_writer.close()


def main():
  print("main")

# # This is a test for parser
#   if len(sys.argv) != 2:
#     print("Usage: VMTranslator.py <inputfile.vm>")
#     return
#   input_path = sys.argv[1]

#   # Test Parser
#   parser = Parser(input_path)
#   while parser.hasMoreLines():
#     print("Current line:", parser.line)
#     cmd_type = parser.commandType()
#     print("Command Type:", cmd_type)
#     if cmd_type != CommandType.C_RETURN:
#       print("Arg1:", parser.arg1())
#     if cmd_type in (CommandType.C_PUSH, CommandType.C_POP, CommandType.C_FUNCTION, CommandType.C_CALL):
#       print("Arg2:", parser.arg2())

# This is a test for parser
  if len(sys.argv) != 2:
    print("Usage: VMTranslator.py <inputfile.vm>")
    return
  input_path = sys.argv[1]

  vmTranslator = VMTranslator(input_path)
  vmTranslator.start()

if __name__=='__main__':
  main()