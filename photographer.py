from picamera import PiCamera
import sys
import subprocess
from astral_calculator import *
from sunny_conf import *
from time import sleep

# the Picamera
camera = PiCamera()
camera.resolution = (3280, 2464)

def the_camera(no_of_frames, delay=8):
    camera.start_preview()
    sleep(2) # Camera warm-up time
    for i in range(no_of_frames):
        file_path = "/home/pi/sunrise2.0/images/" + 'IMAGE_' '{0:04d}'.format(i)+".JPG"
        camera.capture(file_path)
        sleep(delay)
    subprocess.call("touch /home/pi/sunrise2.0/images/end.txt", shell=True)

if __name__ == "__main__":
    print(f"Staring to take {fpd} photos!")
    the_camera(fpd)
    print("Finished")


