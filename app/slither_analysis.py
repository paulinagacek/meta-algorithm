import subprocess, re, os, pickle, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from models import Warning, Vulnerability

def get_warnings(warning_str: str):
    warning_str = warning_str.replace('\n\n', '\n')

    warnings = warning_str.split("Warning:")
    file_name = warnings[0].replace(
        "Compilation warnings/errors on ", "").replace(":", "")

    out = []
    for idx, w in enumerate(warnings[1:]):
        lines = w.split('\n')
        name = lines[0].strip()

        lines[1] = lines[1].strip()
        line = ""
        if re.search('--> .*\.sol:', lines[1]):
            line = int(re.sub('--> .*\.sol:', '', lines[1]).split(':')[:-1][0])

        code_str = ""
        if len(lines) > 3:
            code_str = re.sub('.*\|', '', lines[3])

        out.append(Warning(id=idx, name=name, line=line, code_str=code_str))
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

def deleteFileInfo(vur: str) -> str:
    return re.sub('\([^\(\)#]+#\d*(-\d*)?\)', '', vur)


def get_vulnerabilities(varnabilities_str: str):
    varnabilities_str = re.sub('\n', '<br>', varnabilities_str)
    varnabilities_str = re.sub('\t-', '- &emsp;', varnabilities_str)
    
    varnabilities_str = re.sub('\\x1b\[91m<br>', '***(critical)', varnabilities_str)
    varnabilities_str = re.sub('\\x1b\[92m<br>', '***(suggestion)', varnabilities_str)
    varnabilities_str = re.sub('\\x1b\[93m<br>', '***(medium)', varnabilities_str)

    vulnerabilities = varnabilities_str.split('***')[1:]

    if vulnerabilities:
        vulnerabilities[0] = re.sub('^<br>', '', vulnerabilities[0])
    
    vur_objects = []
    for idx, vur in enumerate(vulnerabilities):
        content, reference = vur.split('Reference: ', 1)[:2]
        reference = re.sub('<br>', '', reference)
        impact, content = deleteFileInfo(content).split(")", 1)
        vur_objects.append(Vulnerability(id=idx, name=content, impact=impact[1:], reference=reference))

    return vur_objects


def analyse_slither(file_name):
    cmd = ('slither', file_name)
    p = subprocess.run(cmd, capture_output=True, text=True)
    # print(p.stderr)
    
    warning_str = extract_warning_str(p.stderr)
    warnings = get_warnings(warning_str)

    vulnerabilities_str = extract_vulnerabilities_str(p.stderr)
    vulnerabilities = get_vulnerabilities(vulnerabilities_str)

    parent_dir_path = os.path.dirname(os.path.realpath(__file__))
    temp_dir = os.path.join(parent_dir_path, 'temp')
    if not os.path.exists(temp_dir):
        os.mkdir(temp_dir)

    with open(os.path.join(temp_dir, 'warnings.pickle'), 'wb') as handle:
        pickle.dump(warnings, handle, protocol=pickle.HIGHEST_PROTOCOL)

    with open(os.path.join(temp_dir, 'vulnerabilities.pickle'), 'wb') as handle:
        pickle.dump(vulnerabilities, handle, protocol=pickle.HIGHEST_PROTOCOL)

if __name__ == '__main__':
    analyse_slither(file_name= r'./example_contracts/slither_vur.sol')