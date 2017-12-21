import pickle
import subprocess

def exec_command(command, _print):
    if _print:
        print("\n[exec command] {}\n:".format(command))
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    process.wait()
    if _print:
        for line in process.stdout:
            print(line)
def write_plk(path, data):
    with open(path , 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
    return path
def read_plk(path):
    with open(path , 'rb') as handle:
        b = pickle.load(handle)
    return b
