import subprocess # to run file cleanup after the upload
from config import *    # my dropbox API key and Push bullet API key
from time import strftime, sleep
from glob import glob

def watcher():
    full_file_list = sorted(glob("/home/pi/sunrise2.0/images/*"))
    folder_name = strftime("/dayimages/")
    for i in full_file_list:
        success = subprocess.call(f"sshpass -p {password} scp {i} {localpath}{folder_name}{i[27:]}", shell = True)
        if success == 0:
            subprocess.call(f"rm -r {i}", shell=True)

if __name__ == "__main__":
    while True:
        sleep(30)
        watcher()
