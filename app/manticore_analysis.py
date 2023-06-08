import subprocess, os, sys, re, pickle
from os.path import join

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
parent_dir_path = os.path.dirname(os.path.realpath(__file__))
temp_dir = join(parent_dir_path, 'temp')

def analyse_manticore(file_name):
    cmd = ('manticore-verifier', file_name, '--propre', 'echidna', '--timeout', '300')
    p = subprocess.run(cmd, capture_output=True, text=True)
    manticore_log = p.stdout

    tests = []
    if '|\n' not in manticore_log:
        tests.append(['ERROR', 'failed'])
    else:
        table = manticore_log.split('|\n', 1)[1].split('+\n', 1)[1].split('\n+', 1)[0]
        table = table.replace('|', '')
        rows = table.split('\n')
        
        for row in rows:
            tests.append(re.findall(r'\w+',  row.strip()))
    
    with open(join(temp_dir, 'manticore_tests.pickle'), 'wb') as handle:
        pickle.dump(tests, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    with open(join(temp_dir, 'manticore_log.pickle'), 'wb') as handle:
        pickle.dump(manticore_log, handle, protocol=pickle.HIGHEST_PROTOCOL)

if __name__ == '__main__':
    analyse_manticore('./example_contracts/echidna2.sol')