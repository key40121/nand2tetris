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
    return

  def writePushPop(self, command, segment, index):
    """
    Writes to the output file the assembly code that implements the given push or pop command.
    """
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

  


def main():
  print("main")

# This is a test for parser
  if len(sys.argv) != 2:
    print("Usage: VMTranslator.py <inputfile.vm>")
    return
  input_path = sys.argv[1]

  # Test Parser
  parser = Parser(input_path)
  while parser.hasMoreLines():
    print("Current line:", parser.line)
    cmd_type = parser.commandType()
    print("Command Type:", cmd_type)
    if cmd_type != CommandType.C_RETURN:
      print("Arg1:", parser.arg1())
    if cmd_type in (CommandType.C_PUSH, CommandType.C_POP, CommandType.C_FUNCTION, CommandType.C_CALL):
      print("Arg2:", parser.arg2())

if __name__=='__main__':
  main()