from JackTokenizer import Keyword

class SymbolTable:
    def __init__(self):
        self.table = {}
        self.index_counters = {
            'static': 0,
            'field': 0,
            'arg': 0,
            'var': 0
        }

    def reset(self):
        """Empties the symbol table, typically called when starting to compile a new subroutine."""
        self.table.clear()
        for key in self.index_counters:
            self.index_counters[key] = 0
        return

    def define(self, name, type, kind):
        """
        Defines (add to the table) a new variable of the given name, type and kind. Assign to it the index value of that kind, and add 1 to the index
        """
        index = self.index_counters[kind]
        self.table[name] = (type, kind, index)
        self.index_counters[kind] += 1

    def varCount(self, kind)-> int:
        """Returns the number of variables of the given kind already defined in the table."""
        return self.index_counters[kind]

    def kindOf(self, name) -> Keyword:
        """Returns the kind of the named identifier. If the identifier is unknown, returns NONE."""
        if name in self.table:
            return self.table[name][1]
        return None

    def typeOf(self, name) -> str:
        """Returns the type of the named identifier. If the identifier is unknown, returns NONE."""
        if name in self.table:
            return self.table[name][0]
        return None

    def indexOf(self, name) -> int:
        """Returns the index of the named identifier."""
        if name in self.table:
            return self.table[name][2]
        return None
    
    def show(self):
        """For debugging: prints the current symbol table."""
        print("\nSymbol Table:")
        for name, (type, kind, index) in self.table.items():
            print(f"{name}: type={type}, kind={kind}, index={index}")
        print("\n")