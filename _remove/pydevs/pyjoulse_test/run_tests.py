import sys

sys.path.append("/home/yimoning/research/util/")
import subprocess

import constants as uc

bash_script_path = "/home/yimoning/research/pydevs/pyjoulse_test/schedule"
if __name__ == "__main__":
    for i in range(50):
        for j in range(50):
            uc.CELLSIZE = i
            uc.SIMROUND = j
            FILE_NAME = str(i) + "*" + str(i) + "_" + str(j) + "times.csv"
            subprocess.run([bash_script_path])