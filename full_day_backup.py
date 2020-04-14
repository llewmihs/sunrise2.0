import subprocess # to run file cleanup after the upload
from config import *    # my dropbox API key and Push bullet API key
from time import strftime
from glob import glob

full_file_list = glob("/home/pi/sunrise2.0/images/*.JPG")
folder_name = strftime("/%d-%b")

for i in full_file_list:
    subprocess.call(f"sshpass -p {password} scp {i} {localpath}{folder_name}", shell = True)