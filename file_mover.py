import subprocess # to run file cleanup after the upload
from config import *    # my dropbox API key and Push bullet API key
from time import strftime, sleep
from glob import glob
from pushbullet import Pushbullet
pb = Pushbullet(PUSHBULLET)


def watcher():
    full_file_list = sorted(glob("/home/pi/sunrise2.0/images/*"))
    folder_name = strftime("/dayimages/")
    errors = False
    for i in full_file_list:
        success = subprocess.call(f"sshpass -p {password} scp {i} {localpath}{folder_name}{i[27:]}", shell = True)
        if success == 0:
            print("Successful transfer")
            subprocess.call(f"rm -r {i}", shell=True)
        else:
            errors = True
            print(f"Not successfull, error code {success}")
    return errors


if __name__ == "__main__":
    while True:
        sleep(30)
        errors = watcher()
        if errors == True:
            pb.push_note("Error", "Error during upload from sunrise pi to home pi")
        
