import subprocess # to run file cleanup after the upload
from config import *    # my dropbox API key and Push bullet API key
from time import strftime
from pushbullet import Pushbullet   # notification software to monitor the programme remotely `pip3 install pushbullet.py`
pb = Pushbullet(PUSHBULLET)

def scp_copy(filename, password, localpath):
    subprocess.call(f"sshpass -p {password} scp {filename} {localpath}", shell = True)
    push = pb.push_note("Job Done", "Timelapse Uploaded")
    print("File uploaded")

if __name__ == "__main__":
    scp_copy(filename, password, localpath)
    push = pb.push_note("Job Done", "Timelapse Uploaded")