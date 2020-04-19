from picamera import PiCamera
import sys
import subprocess
from sunny_conf import *
from creds import *
from time import sleep
from pushbullet import Pushbullet   # notification software to monitor the programme remotely `pip3 install pushbullet.py`
pb = Pushbullet(PUSHBULLET)

# the Picamera
camera = PiCamera()
camera.resolution = (3280, 2464)

def clean_up():
    subprocess.call("rm -r /home/pi/sunrise2.0/images/*", shell=True)
    subprocess.call("rm -r /home/pi/sunrise2.0/sunset/*", shell=True)
    subprocess.call("rm -r /home/pi/sunrise2.0/sunrise/*", shell=True)
    subprocess.call("rm -r /home/pi/sunrise2.0/timelapses/*", shell=True)

def the_camera(no_of_frames, delay=8):
    camera.start_preview()
    sleep(2) # Camera warm-up time
    for i in range(no_of_frames):
        if i <= 800:
            file_path = "/home/pi/sunrise2.0/sunrise/" + 'IMAGE_' '{0:04d}'.format(i)+".JPG"
        elif i == 800:
            subprocess.call("touch /home/home/pi/sunrise2.0/sunrise/end.txt", shell = True) 
        elif 800 < i < (no_of_frames - 800):
            file_list = sorted(glob("/home/pi/sunrise2.0/dayimages/*.JPG"))
            if len(file_list) >= 400:
                subprocess.call(f"rm -r {file_list[0]}")
        file_path = "/home/pi/sunrise2.0/daytime/" + 'IMAGE_' '{0:04d}'.format(i)+".JPG"
        camera.capture(file_path)
        sleep(delay)
    subprocess.call("touch /home/pi/sunrise2.0/images/end.txt", shell=True)

if __name__ == "__main__":
    clean_up()
    print(f"Starting to take {fpd} photos!")
    push = pb.push_note("Today's Photographer Has Started", f"Total frames: {fpd}. Delay: 8.")
    the_camera(fpd)
    print("Finished")


