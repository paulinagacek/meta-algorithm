import subprocess, re, os

class Warning:
    def __init__(self, name, line=None, code_str=None) -> None:
        self.name = name
        self.line = line
        self.code_str = code_str

    def __str__(self):
        return f'{self.name}\nLine:{str(self.line)}\n'

    def __repr__(self):
        return f'({self.name}, Line:{str(self.line)},\nCode: {self.code_str})\n'

class Vulnerability:
    def __init__(self, name, reference=None) -> None:
        self.name = name
        self.reference = reference
    
    def __str__(self):
        return f'{self.name}\nReference:{str(self.reference)}\n'

    def __repr__(self):
        return f'({self.name}, Reference:{str(self.reference)}\n'

def get_warnings(warning_str: str):
    warning_str = warning_str.replace('\n\n', '\n')

    warnings = warning_str.split("Warning:")
    file_name = warnings[0].replace(
        "Compilation warnings/errors on ", "").replace(":", "")

    out = []
    for w in warnings[1:]:
        lines = w.split('\n')
        name = lines[0].strip()

        lines[1] = lines[1].strip()
        line = ""
        if re.search('--> .*\.sol:', lines[1]):
            line = int(re.sub('--> .*\.sol:', '', lines[1]).split(':')[:-1][0])

        code_str = ""
        if len(lines) > 3:
            code_str = re.sub('.*\|', '', lines[3])

        out.append(Warning(name=name, line=line, code_str=code_str))
    return out


def extract_warning_str(entire_log: str) -> str:
    '''
    Return string with warning logs from entire log.
    '''

    if re.search('Compilation warnings/errors on', entire_log) and re.search('Warning:', entire_log):
        if re.search('\n\n\n', entire_log):
            return entire_log.split("\n\n\n", 1)[0]
        else:
            return entire_log
    else:
        return ''


def extract_vulnerabilities_str(entire_log: str) -> str:
    if re.search('analyzed (.* contracts with .* detectors)', entire_log):
        return entire_log.split("\n\n\n", 1)[1]
    else:
        return ''


def get_vulnerabilities(varnabilities_str: str):
   
    varnabilities_str = re.sub('\n', '<br>', varnabilities_str)
    varnabilities_str = re.sub('\t-', '- &emsp;', varnabilities_str)
    varnabilities_str = re.sub('\\x1b\[(91|92|0)m', '', varnabilities_str)
    vulnerabilities = varnabilities_str.split('<br><br>')

    if vulnerabilities:
        vulnerabilities[0] = re.sub('^<br>', '', vulnerabilities[0])
    
    vur_objects = []
    for vur in vulnerabilities:
        content, reference = vur.split('Reference: ', 1)[:2]
        reference = re.sub('<br>', '', reference)
        vur_objects.append(Vulnerability(name=content, reference=reference))

    return vur_objects


def catch_output(file_name):
    cmd = ('slither', file_name)
    p = subprocess.run(cmd, capture_output=True, text=True)
    
    warning_str = extract_warning_str(p.stderr)
    vulnerabilities_str = extract_vulnerabilities_str(p.stderr)

    return get_warnings(warning_str), get_vulnerabilities(vulnerabilities_str)


if __name__ == '__main__':
    catch_output()
