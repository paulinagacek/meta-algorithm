import subprocess, re, os, pickle, sys, shutil
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

def analyse_echidna(file_name):
    parent_dir_path = os.path.dirname(os.path.realpath(__file__))
    shutil.rmtree(parent_dir_path + '/temp/echidna')
    cmd = ('echidna', file_name, '--corpus-dir', 'app/temp/echidna')
    p = subprocess.run(cmd, capture_output=True, text=True)
    fuzzing_log = p.stdout

    with open(parent_dir_path + '/temp/fuzzing_log.pickle', 'wb') as handle:
        pickle.dump(fuzzing_log, handle, protocol=pickle.HIGHEST_PROTOCOL)
    print(fuzzing_log)

if __name__ == '__main__':
    analyse_echidna(file_name= r'./example_contracts/echidna2.sol')