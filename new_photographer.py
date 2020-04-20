from glob import glob
import sys # for argv
from picamera import PiCamera
import subprocess
from time import sleep, strftime
from config import *

# the Picamera
camera = PiCamera()
camera.resolution = (3280, 2464)

# create subfolders
if sys.argv > 1:
    folder_name = sys.argv[1]
    folder_date = strftime("%d%b")
    folder_name = folder_date + folder_name
    full_path = "/home/pi/sunrise2.0/" + folder_name + "/"
    subprocess.call(f"mkdir folder_name", shell = True)

def scp_copy(filename, password, localpath):
    subprocess.call(f"sshpass -p {password} scp {filename} {localpath}", shell = True)
    push = pb.push_note("Job Done", "Timelapse Uploaded")
    print("File uploaded")

def timelapse_camera(folder, full_path):
    camera.start_preview()
    sleep(2) # Camera warm-up time
    for i in range(900):
        photo_name = strftime("%Y%m%d-%H%M%S.JPG")
        camera.capture(full_path+photo_name)
        sleep(8)
    full_file_list = sorted(glob(f"/home/pi/sunrise2.0/{sys.argv[1]}/*"))
    for j in full_file_list:
        subprocess.call(f"sshpass -p {password} scp {filename} {localpath}", shell = True)
    




