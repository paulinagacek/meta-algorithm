import subprocess
import re
class Warning:
    def __init__(self, name, line_and_char=None, code_str=None) -> None:
        self.name = name
        self.line_and_char = line_and_char
        self.code_str = code_str
    
    def __str__(self):
        return f'{self.name}\nLines:char:{str(self.line_and_char)}\n'
    
    def __repr__(self):
        return f'({self.name}, Lines:char:{str(self.line_and_char)},\nCode: {self.code_str})\n'


def get_warnings(warning_str: str):
    warning_str = warning_str.replace('\n\n\n\n', '\n').replace('\n\n', '\n')
    warning_str = warning_str.split("INFO:Detectors:")[0]
    warnings = warning_str.split("Warning:")
    file_name = warnings[0].replace("Compilation warnings/errors on ", "").replace(":", "")
    print("file name:", file_name)
    out = []
    for w in warnings[1:]:
        lines = w.split('\n')
        name = lines[0].strip()

        lines[1] = lines[1].strip()
        line_and_char=""
        if re.search('--> .*\.sol', lines[1]):
            line_and_char = tuple(re.sub('--> .*\.sol:', '', lines[1]).split(':')[:-1])
        
        code_str=""
        if len(lines) > 3:
            code_str = re.sub('.*\|', '', lines[3].strip()).strip()

        out.append(Warning(name=name, line_and_char=line_and_char, code_str=code_str))
    print(out)
    return out

if __name__ == '__main__':
    cmd = ('slither', '.\\example_contracts\\test_arithmetic.sol')
    p = subprocess.run(cmd, capture_output=True, text=True)
    print("---")
    warnings = get_warnings(p.stderr)