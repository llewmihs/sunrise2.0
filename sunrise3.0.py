# To do: Check if it's a sunrise or sunset
from sys import argv
from time import strftime, sleep
from picamera import Picamera
from subprocess import call
from os import makedirs, path
from glob import glob
from creds import password, localpath

camera = PiCamera()
camera.resolution = (3280, 2464)

def take_900_images(full_folder_path, rise_or_set, delay=8):
    camera.start_preview()
    sleep(2)
    for i in range(900):
        photo_filename = strftime(f"{full_folder_path}{rise_or_set}_IMAGE_%Y%m%d%H%M%S.JPG")
        camera.capture(photo_filename)
        sleep(delay)

def upload_to_ilfrastore(full_folder_path):


if __name__ == "__main__":
    #check if we are running a sunrise or sunset
    if argv > 1:
        rise_or_set = argv[1]
        print(f"Running a {rise_or_set}")
    
    # create the proper storage folders
    root_folders = "/home/pi/sunrise2.0"
    folder_name = strftime(f"/%Y%m%d-{rise_or_set}/")
    full_folder_path = root_folders + folder_name
    if not path.exists(full_folder_path):
        makedirs(full_folder_path)
    
    # take the 900 photos needed
    take_900_images(full_folder_path, rise_or_set)

    # upload the files to store
    full_file_list = sorted(glob(f"{full_folder_path}*.JPG"))
    counter = 0
    for i in full_file_list:
        subprocess.call(f"sshpass -p {password} scp {i} {localpath}{folder_name}{i[27:]}", shell = True)
        counter +=
    
    # run ffmepg and upload the result


    # once the programme has ended, reset the cront if it was a sunset
    if rise_or_set == "sunset":
        # code in here to update the crontab