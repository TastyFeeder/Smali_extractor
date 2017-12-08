
import subprocess

def exec_command(command, _print):
    if _print:
        print("\n[exec command] {}\n:".format(command))
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    process.wait()
    if _print:
        for line in process.stdout:
            print(line)
