from enum import Enum
import sys
import os
from pathlib import Path

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
    if self.line.startswith("eq") or self.line.startswith("add") or self.line.startswith("sub") or self.line.startswith("neg") or self.line.startswith("gt") or self.line.startswith("lt") or self.line.startswith("and") or self.line.startswith("or") or self.line.startswith("not"):
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
    If the current command is C_LABEL, C_GOTO, or C_IF, the label is returned.
    Returns:
      str: The first argument or command.
    """

    divided_line = self.line.split()
    if self.commandType() == CommandType.C_ARITHMETIC:
      return divided_line[0]
    return divided_line[1]
  
  def arg2(self):
    """
    Returns the second argument of the current command.
    """
    if self.commandType() in (CommandType.C_PUSH, CommandType.C_POP, CommandType.C_FUNCTION, CommandType.C_CALL):
      divided_line = self.line.split()
      return int(divided_line[2])

    if self.commandType() not in (CommandType.C_PUSH, CommandType.C_POP, CommandType.C_FUNCTION, CommandType.C_CALL):
      print("Error: arg2 called on invalid command type")
      return

  def close(self):
    """Closes the input file."""
    self.file.close()


class CodeWriter:
  def __init__(self, file_name=None):
    """
    This class handles the output file
    """
    self.file = None
    self.label_counter = 0
    self.current_file_name = None
    if file_name:
      self.file = open(file_name + '.asm', 'w', encoding='utf-8')
    
  def setFileName(self, file_name):
    """Sets the current file name for static segment handling."""
    self.current_file_name = Path(file_name).stem
    
  def writeBootstrap(self):
    """Writes the bootstrap code."""
    self.file.write("// Bootstrap code\n")
    self.file.write("@256\n")
    self.file.write("D=A\n")
    self.file.write("@SP\n")
    self.file.write("M=D\n")
    self.file.write("// call Sys.init\n")
    self.writeCall("Sys.init", 0)

  def writeArithmetic(self, command):
    """
    Writes to the output file the assembly code that implements the given arithmetic-logical command.
    """
    if command not in ['add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not']:
      print("Error: Invalid command for writeArithmetic:", command)
      return

    if command == 'add':
      self.file.write("\n\n")
      self.file.write("// add\n")
      self.file.write("@SP\n")
      self.file.write("M=M-1\n") # SP--
      self.file.write("A=M\n") # A = SP (now points to top value y)
      self.file.write("D=M\n")  # D = y
      self.file.write("A=A-1\n") # A = SP - 1 (now points to next value x)
      self.file.write("M=D+M\n")  # M = x + y
      return

    elif command == 'sub':
      self.file.write("\n\n")
      self.file.write("// sub\n")
      self.file.write("@SP\n")
      self.file.write("M=M-1\n") # SP--
      self.file.write("A=M\n") # A = SP (now points to top value y)
      self.file.write("D=M\n")  # D = y
      self.file.write("A=A-1\n") # A = SP - 1 (now M points to x)
      self.file.write("M=M-D\n")  # M = x - y
      return

    elif command == 'neg':
      self.file.write("\n\n")
      self.file.write("// neg\n")
      self.file.write("@SP\n")
      self.file.write("A=M-1\n")
      self.file.write("M=-M\n")
      return
    
    elif command in ('eq', 'gt', 'lt'):
      self.file.write("\n\n")
      jump = {'eq': 'JEQ', 'gt': 'JGT', 'lt': 'JLT'}[command]
      true_label = f"{command.upper()}_TRUE{self.label_counter}"
      end_label = f"{command.upper()}_END{self.label_counter}"
      self.label_counter += 1
      self.file.write(f"// {command}\n")
      self.file.write("@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\n")
      self.file.write(f"@{true_label}\nD;{jump}\n")
      self.file.write("@SP\nA=M-1\nM=0\n")
      self.file.write(f"@{end_label}\n0;JMP\n")
      self.file.write(f"({true_label})\n@SP\nA=M-1\nM=-1\n")
      self.file.write(f"({end_label})\n")
      return
    
    elif command == 'and':
      self.file.write("// and\n")
      self.file.write("@SP\n")
      self.file.write("AM=M-1\n")
      self.file.write("D=M\n")
      self.file.write("A=A-1\n")
      self.file.write("M=D&M\n")  # *SP = *SP & D
      return
    
    elif command == 'or':
      self.file.write("//or\n")
      self.file.write("@SP\n")
      self.file.write("AM=M-1\n")
      self.file.write("D=M\n")
      self.file.write("A=A-1\n")
      self.file.write("M=D|M\n")  # *SP = *SP | D
      return
    elif command == 'not':
      self.file.write("\n\n")
      self.file.write("// not\n")
      self.file.write("@SP\n")
      self.file.write("A=M-1\n")
      self.file.write("M=!M\n")  # *SP = !(*SP)
      return

  def writePushPop(self, commandType, segment, index):
    """
    Writes to the output file the assembly code that implements the given push or pop command.
    """
    if commandType not in ['C_PUSH', 'C_POP']:
      print("Error: Invalid command for writePushPop:", commandType)
      return
    
    if commandType == 'C_PUSH':
      self.file.write("\n\n")
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
        # Use file-specific static segment addresses
        static_addr = 16 + (ord(self.current_file_name[0]) % 240)  # Generate unique address per file
        self.file.write(f"// D = RAM[{static_addr + index}]\n")
        self.file.write(f"@{static_addr + index}\n")
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
      self.file.write("\n\n")
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
        # Use file-specific static segment addresses
        static_addr = 16 + (ord(self.current_file_name[0]) % 240)  # Generate unique address per file
        self.file.write(f"// SP--\n")
        self.file.write("@SP\n")
        self.file.write("AM=M-1\n")
        self.file.write("D=M\n")  # D = *SP
        self.file.write(f"// RAM[{static_addr + index}] = RAM[SP]\n")
        self.file.write(f"@{static_addr + index}\n")
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
    
  def writeLabel(self, label):
    """Writes assembly code that effects the label command."""
    self.file.write("// label\n")
    self.file.write(f"({label})\n")
    self.file.write("\n")

  def writeGoto(self, label):
    """Writes assembly code that effects the goto command."""
    self.file.write("// goto\n")
    self.file.write(f"@{label}\n")
    self.file.write("0;JMP\n")
    self.file.write("\n")

  def writeIf(self, label):
    """Writes assembly code that effects the if-goto command."""
    self.file.write("// if-goto\n")
    self.file.write("@SP\n")
    self.file.write("M=M-1\n")  # SP--
    self.file.write("A=M\n")    # A=SP
    self.file.write("D=M\n")    # D=*SP
    self.file.write(f"@{label}\n")
    self.file.write("D;JNE\n")   # if D != 0 jump to label
    self.file.write("\n")

  def writeFunction(self, functionName, numLocals):
    """Writes assembly code that effects the function command."""
    self.file.write(f"// function {functionName} {numLocals}\n")
    self.file.write(f"({functionName})\n")
    # Initialize local variables to 0
    for i in range(numLocals):
      self.file.write("@SP\n")
      self.file.write("A=M\n")
      self.file.write("M=0\n")
      self.file.write("@SP\n")
      self.file.write("M=M+1\n")

  def writeCall(self, functionName, numArgs):
    """Writes assembly code that effects the call command."""
    return_address = f"{functionName}$ret.{self.label_counter}" # to ensure unique return address
    self.label_counter += 1

    # Push return address
    self.file.write("// call\n")
    self.file.write(f"@{return_address}\n") # created by compiler
    self.file.write("D=A\n")
    self.file.write("@SP\n")
    self.file.write("A=M\n")
    self.file.write("M=D\n")
    self.file.write("@SP\n")
    self.file.write("M=M+1\n")
    self.file.write("\n")

    # Push LCL, ARG, THIS, THAT
    for segment in ['LCL', 'ARG', 'THIS', 'THAT']:
      self.file.write(f"// push {segment}\n")
      self.file.write(f"@{segment}\n")
      self.file.write("D=M\n")
      self.file.write("@SP\n")
      self.file.write("A=M\n")
      self.file.write("M=D\n")
      self.file.write("@SP\n")
      self.file.write("M=M+1\n")
      self.file.write("\n")

    # Reposition ARG
    self.file.write("// Reposition ARG\n")
    self.file.write("@SP\n")
    self.file.write("D=M\n")
    self.file.write(f"@{numArgs + 5}\n") # not address but value in A
    self.file.write("D=D-A\n")
    self.file.write("@ARG\n")
    self.file.write("M=D\n")
    self.file.write("\n")

    # Reposition LCL
    self.file.write("// Reposition LCL\n")
    self.file.write("@SP\nD=M\n")
    self.file.write("@LCL\nM=D\n")
    self.file.write("\n")

    # Transfer control
    self.file.write(f"@{functionName}\n")
    self.file.write("0;JMP\n")
    self.file.write(f"({return_address})\n")
    self.file.write("\n")

  def writeReturn(self):
    """Writes assembly code that effects the return command."""
    # FRAME = LCL
    self.file.write("// return\n")
    self.file.write("// FRAME = LCL\n")
    self.file.write('@LCL\n')
    self.file.write("D=M\n")
    self.file.write("@R13\n")
    self.file.write("M=D\n")  # R13 = FRAME

    # RET = *(FRAME-5)
    self.file.write("// RET = *(FRAME-5)\n")
    self.file.write("@5\n")
    self.file.write("A=D-A\n")
    self.file.write("D=M\n")
    self.file.write("@R14\n")
    self.file.write("M=D\n")  # R14 = RET

    # *ARG = pop()
    self.file.write("@SP\nAM=M-1\nD=M\n")
    self.file.write("@ARG\nA=M\nM=D\n")

    # SP = ARG + 1
    self.file.write("@ARG\nD=M+1\n")
    self.file.write("@SP\nM=D\n")

    # THAT = *(FRAME-1)
    self.file.write("@R13\nAM=M-1\nD=M\n")
    self.file.write("@THAT\nM=D\n")

    # THIS = *(FRAME-2)
    self.file.write("@R13\nAM=M-1\nD=M\n")
    self.file.write("@THIS\nM=D\n")

    # ARG = *(FRAME-3)
    self.file.write("@R13\nAM=M-1\nD=M\n")
    self.file.write("@ARG\nM=D\n")

    # LCL = *(FRAME-4)
    self.file.write("@R13\nAM=M-1\nD=M\n")
    self.file.write("@LCL\nM=D\n")

    # goto RET
    self.file.write("@R14\nA=M\n0;JMP\n")

  def close(self):
    """Closes the output file."""
    if self.file:
      self.file.close()

class VMTranslator:
  def __init__(self, input_path, is_directory=False):
    self.input_path = input_path
    self.is_directory = is_directory
    self.vm_files = []
    
    if is_directory:
      # Get all .vm files, with Sys.vm first
      dir_path = Path(input_path)
      all_files = sorted(dir_path.glob('*.vm'))
      
      # Separate Sys.vm and others
      sys_files = [f for f in all_files if f.stem == 'Sys']
      other_files = [f for f in all_files if f.stem != 'Sys']
      
      # Sys.vm should be first
      self.vm_files = sys_files + other_files
      
      # Output file is directory name + .asm
      output_name = dir_path.name
      self.code_writer = CodeWriter(str(dir_path / output_name))
    else:
      self.vm_files = [Path(input_path)]
      output_name = Path(input_path).stem
      self.code_writer = CodeWriter(output_name)

  def start(self):
    # Write bootstrap code if directory
    if self.is_directory:
      self.code_writer.writeBootstrap()
    
    # Translate each file
    for vm_file in self.vm_files:
      self.translateFile(str(vm_file))
    
    self.code_writer.close()

  def translateFile(self, file_path):
    """Translate a single VM file."""
    parser = Parser(file_path)
    self.code_writer.setFileName(file_path)
    
    while parser.hasMoreLines():
      command_type = parser.commandType()
      if command_type == CommandType.C_ARITHMETIC:
        command = parser.arg1()
        self.code_writer.writeArithmetic(command)
      elif command_type in (CommandType.C_PUSH, CommandType.C_POP):
        segment = parser.arg1()
        index = parser.arg2()
        self.code_writer.writePushPop(command_type.name, segment, index)
      elif command_type == CommandType.C_LABEL:
        label = parser.arg1()
        self.code_writer.writeLabel(label)
      elif command_type == CommandType.C_GOTO:
        label = parser.arg1()
        self.code_writer.writeGoto(label)
      elif command_type == CommandType.C_IF:
        label = parser.arg1()
        self.code_writer.writeIf(label)
      elif command_type == CommandType.C_FUNCTION:
        function_name = parser.arg1()
        num_locals = parser.arg2()
        self.code_writer.writeFunction(function_name, num_locals)
      elif command_type == CommandType.C_CALL:
        function_name = parser.arg1()
        num_args = parser.arg2()
        self.code_writer.writeCall(function_name, num_args)
      elif command_type == CommandType.C_RETURN:
        self.code_writer.writeReturn()
    
    parser.close()


def main():
  if len(sys.argv) != 2:
    print("Usage: VMTranslator.py <inputfile.vm or directory>")
    return
  
  input_path = sys.argv[1]
  path = Path(input_path)
  
  if path.is_dir():
    # Directory mode - translate all .vm files with bootstrap
    vmTranslator = VMTranslator(input_path, is_directory=True)
  elif path.is_file() and path.suffix == '.vm':
    # Single file mode - no bootstrap
    vmTranslator = VMTranslator(input_path, is_directory=False)
  else:
    print("Error: Input must be a directory or a .vm file")
    return
  
  vmTranslator.start()

if __name__=='__main__':
  main()