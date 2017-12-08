import sys
import os
from os.path import isfile, join
from os import listdir
from termcolor import colored, cprint
import numpy as np
import ntpath
import subprocess
import time
import pickle
from utils import exec_command

tmp_sufix = "../tmp"
api_list_path = "../data/apilist.plk"
dex2jar_path = "~/tool/dex2jar/"
j2dex_command = "d2j-jar2dex.sh"
dex2smali_command = "d2j-dex2smali.sh"
print_command = True
api_list = []
total_api = []
py_path = os.path.dirname(os.path.abspath(__file__))
# Read api list from file
total_api = pickle.load(open(os.path.join(py_path, api_list_path), "rb"))


cb_flag = False
invoke_type = ['invoke-static','invoke-virtual','invoke-direct','invoke-super']
def extract_apk(apk_path):
    tmp_path = os.path.join(py_path, tmp_sufix)
    myapk = apk_info(apk_path, tmp_path)
# TODO : here output path is fix under [this py file]/../tmp/[apkname].out maybe change th     input argv or something
    output_path = os.path.join(tmp_path, myapk.base) + ".out"
#add script of apktools here
    apktool_prefix = "apktool"
    command = ""
    command += apktool_prefix
    command += " d "
    command += apk_path
    command += " -o {}".format(myapk.output_path)
    exec_command(command, print_command)


# parse smali and save to proper type(matrix?)
    if(os.path.exists(myapk.walk)):
        myapk.iter_all_smali(myapk.walk)
    else:
#        exec_dir = os.path.join(os.path.join(dir_name, base_name) + ".out","unknown")
        smali_path = myapk.gen_smali_from_class(myapk.exec_dir, myapk.base)
        myapk.iter_all_smali(smali_path)


    #for root, subdirs, files in os.walk(walk_dir):
    print(api_list)
    print(len(api_list))
# remove data from apktool
    command = ""
    command += "rm "
    command += "-rf "
    command += myapk.output_path
    exec_command(command, print_command)






# TODO put all info(ex:matrix) and extract function here
class apk_info:
    def __init__(self, path, tmp_path):
        self.path = path
        self.base = ntpath.basename(path)
        self.output_path = os.path.join(tmp_path, self.base) + ".out"
        self.direct = os.path.dirname(os.path.abspath(path))
        self.walk = os.path.join(self.output_path, "smali")
        self.exec_dir = os.path.join(self.output_path, "unknown")

# TODO:exec_command is relate outer function should be handle
    def gen_smali_from_class(self, path, base_name):
        print("path:   ", path)
        jar_pos = os.path.join(path, base_name)
        command = ""
        command += "jar cf"
        command += " "
        command += jar_pos + ".jar"
        command += " "
        command += os.path.join(path, "*.class")
        exec_command(command, print_command)
        command = ""
        command += os.path.join(dex2jar_path, j2dex_command)
        command += " -f "
        command += " -f "
        command += jar_pos + ".jar"
        command += " -o "
        command += jar_pos + "-jar2dex.dex"
        exec_command(command, print_command)

        command = ""
        command += os.path.join(dex2jar_path, dex2smali_command)
        command += " "
        command += jar_pos + "-jar2dex.dex"
        command += " -o "
        command += jar_pos + "-jar2dex.out"
        exec_command(command, print_command)

        return os.path.join(path, jar_pos + "-jar2dex.out")


# check every smali under walk_dir
    def iter_all_smali(self, walk_dir):
        for root, subdirs, files in os.walk(walk_dir):
            for f in files:
                if f.endswith(".smali"):
                    self.check_smali(os.path.join(root, f))
            #for fold in subdirs:
            #    iter_all_smali(os.path.join(root, fold))
            #    print(os.path.join(root, fold))

# TODO : select printable 
    def check_smali(self, path):

        fin = open(path, 'r')
        raw_data = fin.read().split('\n')
        print("check: ",path)
        cb_flag = False
        for line in raw_data:
            data = line.split(' ')
            while '' in data:
                data.remove('')
            if data  == []:
                continue
            if data[0].startswith('.method'):
                print("\t[code block] start {}".format(data[1:]))
                cb_flag = True
                continue

            if data[0].startswith('.end') and data[1] == 'method':
                print("\t[code block] end",data[1:])
                cb_flag = False
                continue
            if cb_flag:
                self.check_api(data)
        return

    def is_normal(self, L):
        if not L.startswith("Lcom") and not L.startswith("Landroid") and not L.startswith(    "Ljava") and not L.startswith("Ldalvik") and not L.startswith("Lorg"):
            return True
        return False
# check is api from android ?        
    def is_api(self, L):
        call_L = L[1:]
        call_L = ".".join(x for x in call_L.split("/")[:-1])
# TODO: var total_api is global var should be handle after this class being packed
        if call_L in total_api:
            return True
        return False


    def check_api(self, data):
    #TODO collect each matrix
        try:
            if data[0] in invoke_type:
                if data[-1].startswith('L'):
                    L = data[-1].split(';')
                    print("\t|  [API] \n\t|---invoke method:{} \n\t  \-->from {} invoke {}    ".format(data[0],L[0],"".join(L[1:])))
#                    self.is_api(L[0])
                    if self.is_api(L[0]):
                        if L[0] not  in api_list:
                            api_list.append(L[0])
                    #print_red_on_cyan("api call {} {}".format(data[0],data[-1]))
        except:
            print("line is {}".format(data))

if __name__ == "__main__":
    apk_path = sys.argv[1]
    extract_apk(apk_path)
    #main()
