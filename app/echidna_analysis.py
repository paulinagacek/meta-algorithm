import subprocess, re, os, pickle, sys, shutil
from os import listdir
from os.path import isfile, join

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
parent_dir_path = os.path.dirname(os.path.realpath(__file__))
print(parent_dir_path)

def analyse_echidna(file_name):
    temp_dir = join(parent_dir_path, 'temp')
    echidna_dir = join(temp_dir, 'echidna')
    if os.path.exists(echidna_dir):
        shutil.rmtree(echidna_dir)
    os.mkdir(echidna_dir)
    
    cmd = ('echidna', file_name, '--corpus-dir', echidna_dir)
    p = subprocess.run(cmd, capture_output=True, text=True)
    fuzzing_log = p.stdout
    print("Fuzzing:")
    print(fuzzing_log, p.stderr)
    print("---")

    with open(join(temp_dir, 'fuzzing_log.pickle'), 'wb') as handle:
        pickle.dump(fuzzing_log, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    print(listdir('./example_contracts'))
    
    coverage_file_name = [f for f in listdir(echidna_dir) if isfile(join(echidna_dir, f)) and f[-4:]=="html"][0]

    print(coverage_file_name)

    with open(join(echidna_dir, coverage_file_name)) as f:
        code_coverage = f.read()
        with open(parent_dir_path + '/temp/code_coverage.pickle', 'wb') as handle:
            pickle.dump(code_coverage, handle, protocol=pickle.HIGHEST_PROTOCOL)

if __name__ == '__main__':
    analyse_echidna('./example_contracts/echidna2.sol')