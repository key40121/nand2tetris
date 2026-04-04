
class Segment:
    CONSTANT = "constant"
    ARGUMENT = "argument"
    LOCAL = "local"
    STATIC = "static"
    THIS = "this"
    THAT = "that"
    POINTER = "pointer"
    TEMP = "temp"

class Command:
    ADD = "add"
    SUB = "sub"
    NEG = "neg"
    EQ = "eq"
    GT = "gt"
    LT = "lt"
    AND = "and"
    OR = "or"
    NOT = "not"

class VMWriter:
    def __init__(self, output_file, encoding='utf-8'):
        self.output_file = output_file
        self.encoding = encoding
        self.indent =  "  "  # for pretty printing, not required by VM spec

    def writePush(self, segment, index):
        """Writes a VM push command."""
        self.output_file.write(f"{self.indent}push {segment} {index}\n")
        return
    
    def writePop(self, segment, index):
        """Writes a VM pop command."""
        self.output_file.write(f"{self.indent}pop {segment} {index}\n")
        return
    
    def writeArithmetic(self, command):
        """Writes a VM arithmetic command."""
        self.output_file.write(f"{self.indent}{command}\n")
        return
    
    def writeLabel(self, label):
        """Writes a VM label command."""
        self.output_file.write(f"label {label}\n")
        return
    
    def writeGoto(self, label):
        """Writes a VM goto command."""
        
        self.output_file.write(f"{self.indent}goto {label}\n")
        return
    
    def writeIf(self, label):
        """Writes a VM if-goto command."""
        self.output_file.write(f"{self.indent}if-goto {label}\n")
        return
    
    def writeCall(self, name, nArgs):
        """Writes a VM call command."""
        self.output_file.write(f"{self.indent}call {name} {nArgs}\n")
        return
    
    def writeFunction(self, name, nLocals):
        """Writes a VM function command."""
        print(f"function {name} {nLocals}", file=self.output_file)
        return
    
    def writeReturn(self):
        """Writes a VM return command."""
        self.output_file.write(f"{self.indent}return\n")
        return
    
    def close(self):        
      """Closes the output file."""
      self.output_file.close()
      return