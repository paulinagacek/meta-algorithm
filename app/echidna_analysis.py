import subprocess, re, os, pickle, sys, shutil
from os import listdir
from os.path import isfile, join

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
parent_dir_path = os.path.dirname(os.path.realpath(__file__))
def count_test_score(fuzzing_log: str):
    passing = len(re.findall(': passing', fuzzing_log))
    failed = len(re.findall(': failed', fuzzing_log))
    # print("passing:", passing, "  failed:", failed)
    return passing, failed


def analyse_echidna(file_name):
    echidna_dir = parent_dir_path + '/temp/echidna'
    if os.path.isdir(echidna_dir):
        shutil.rmtree(echidna_dir)
    cmd = ('echidna', file_name, '--corpus-dir', echidna_dir)
    p = subprocess.run(cmd, capture_output=True, text=True)
    fuzzing_log = p.stdout
    passing, failed = count_test_score(fuzzing_log)
    stats = {
        'passing_nr': passing,
        'failed_nr': failed
    }

    with open(parent_dir_path + '/temp/fuzzing_log.pickle', 'wb') as handle:
        pickle.dump(fuzzing_log, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    with open(parent_dir_path + '/temp/echidna_stats.pickle', 'wb') as handle:
        pickle.dump(stats, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    coverage_file_name = [f for f in listdir(echidna_dir) if isfile(join(echidna_dir, f)) and f[-4:]=="html"][0]

    with open(join(echidna_dir, coverage_file_name)) as f:
        code_coverage = f.read()
        with open(parent_dir_path + '/temp/code_coverage.pickle', 'wb') as handle:
            pickle.dump(code_coverage, handle, protocol=pickle.HIGHEST_PROTOCOL)

if __name__ == '__main__':
    analyse_echidna('./example_contracts/echidna2.sol')