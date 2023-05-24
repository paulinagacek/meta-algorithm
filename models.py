import json

class Warning:
    def __init__(self, id, name, line=None, code_str=None) -> None:
        self.id = id
        self.name = name
        self.line = line
        self.code_str = code_str

    def __str__(self):
        return f'{self.name}\nLine:{str(self.line)}\n'

    def __repr__(self):
        return f'({self.name}, Line:{str(self.line)},\nCode: {self.code_str})\n'

class Vulnerability:
    def __init__(self, id, name, reference=None) -> None:
        self.id = id
        self.name = name
        self.reference = reference
    
    def __str__(self):
        return f'{self.name}\nReference:{str(self.reference)}\n'

    def __repr__(self):
        return f'({self.name}, Reference:{str(self.reference)}\n'
