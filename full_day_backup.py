import subprocess # to run file cleanup after the upload
from config import *    # my dropbox API key and Push bullet API key
from time import strftime
from glob import glob

full_file_list = glob("/home/pi/sunrise2.0/images/*.JPG")
folder_name = strftime("/imagecache/%d-%b")

for i in full_file_list:
    print(f"sshpass -p {password} scp {i} {localpath}{folder_name}")
    subprocess.call(f"sshpass -p {password} scp {i} {localpath}{folder_name}{i[-8:]}", shell = True)