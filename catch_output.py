import subprocess
import re
import os
class Warning:
    def __init__(self, name, line=None, code_str=None) -> None:
        self.name = name
        self.line = line
        self.code_str = code_str
    
    def __str__(self):
        return f'{self.name}\nLine:{str(self.line)}\n'
    
    def __repr__(self):
        return f'({self.name}, Line:{str(self.line)},\nCode: {self.code_str})\n'


def get_warnings(warning_str: str):
    print('output:\n', warning_str, '\n\n----')
    warning_str = warning_str.replace('\n\n\n\n', '\n').replace('\n\n', '\n')
    warning_str = warning_str.split("INFO:Detectors:")[0]
    warnings = warning_str.split("Warning:")
    file_name = warnings[0].replace("Compilation warnings/errors on ", "").replace(":", "")

    out = []
    for w in warnings[1:]:
        lines = w.split('\n')
        name = lines[0].strip()

        lines[1] = lines[1].strip()
        line=""
        if re.search('--> .*\.sol:', lines[1]):
            line = int(re.sub('--> .*\.sol:', '', lines[1]).split(':')[:-1][0])

        code_str=""
        if len(lines) > 3:
            code_str = re.sub('.*\|', '', lines[3])

        out.append(Warning(name=name, line=line, code_str=code_str))
    return out

def catch_warnigns():
    root = os.path.dirname(os.path.abspath(__file__))
    cmd = ('slither', '.\\example_contracts\\lock.sol')
    p = subprocess.run(cmd, capture_output=True, text=True)
    return get_warnings(p.stderr)

if __name__ == '__main__':
    catch_warnigns()