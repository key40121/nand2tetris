from enum import Enum
import fileinput

class InstructionType(Enum):
  A_INSTRUCTION = 1
  C_INSTRUCTION = 2
  L_INSTRUCTION = 3

class Parser:
  def __init__(self, asm_input, encoding='utf-8'):
    self.file = open(asm_input, 'r', encoding=encoding)
    self.next_line = None

  def advance(self):
    """this function returns current line, actually not advancing..."""
    return self.next_line

  def hasMoreLines(self):
    while True:
      line = self.file.readline()
      if not line: # EOF
        return False
      stripped_line = line.split("//", 1)[0].strip()
      if stripped_line != "":
        self.next_line = stripped_line
        return True

  def instructionType(self, current_line):
    if current_line.startswith("@"):
      return InstructionType.A_INSTRUCTION
    elif current_line.startswith("(") and current_line.endswith(")"):
      return InstructionType.L_INSTRUCTION
    else:
      return InstructionType.C_INSTRUCTION

  def symbol(self, current_line):
    instructionType = self.instructionType(current_line)
    if instructionType == InstructionType.A_INSTRUCTION:
      return current_line.split("@")[1]
    elif instructionType == InstructionType.L_INSTRUCTION:
      return current_line[1:-1]
    else: # This is c instruction
      return None
  
  def close(self):
    self.file.close()