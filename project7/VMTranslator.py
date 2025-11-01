from enum import Enum

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
      stripped_line = line.split("//", 1)[0]
      if stripped_line != "":
        self.line = stripped_line
        return True

  def commandType(self) -> CommandType:
    """
    Call after check hasMoreLines == true
    Retuns a constant representing the type of the current command.
    """
    if self.line.startswith("eq") or self.line.startswith("add") or self.line.startswith("sub") or self.line.startswith(""):
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
    if self.commandType() == CommandType.C_RETURN:
      return
    
    divided_line = self.line.split("", 1)
    if self.commandType() == CommandType.C_ARITHMETIC:
      return divided_line[0]
    
    """for other commands"""
    return divided_line[1]
  
  def arg2(self):
    """
    Returns the second argument of the current command.
    Called only if the current command is C_PUSH, C_POP, C_FUNCTION, or C_CALL.
    """
    if self.commandType() in (CommandType.C_PUSH, CommandType.C_POP, CommandType.C_FUNCTION, CommandType.C_CALL):
      divided_line = self.line.split("", 2)
      return int(divided_line[2])
    
    if self.commandType() not in (CommandType.C_PUSH, CommandType.C_POP, CommandType.C_FUNCTION, CommandType.C_CALL):
      print("Error: arg2 called on invalid command type")
      return


class CodeWriter:
  def __init__(self):
    """
    This class handles the output file
    """
    return
  
class VMTranslator:
  def __init__(self, file_name):
    self.file_name = file_name
    self.parser = Parser(file_name)
    self.code_writer = CodeWriter()

  


def main():
  print("Hello World")

  # Test code here

if __name__=='__main__':
  main()