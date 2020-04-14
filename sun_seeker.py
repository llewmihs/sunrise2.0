# this file monitors the file names of the image taken throughout the day
# on two occasions it triggers a ffmepg to create a timelapse

import subprocess
from glob import glob
from sunny_conf import fpd
from time import sleep, strftime
import os
from creds import *
from pushbullet import Pushbullet   # notification software to monitor the programme remotely `pip3 install pushbullet.py`
pb = Pushbullet(PUSHBULLET)
from lapse_uploader import *

push = pb.push_note("Sun_Seeker.py running", "Well done")

sunrise_watch_file = '/home/pi/sunrise2.0/images/IMAGE_0599.JPG'
days_end_file = '/home/pi/sunrise2.0/images/end.txt'

# sunset start file
def sunset_start(fpd):
    file_num = "/home/pi/sunrise2.0/images/IMAGE_" + str(fpd-450) + ".JPG"
    return file_num

def file_most_recent():
    list_of_files = glob('/home/pi/sunrise2.0/images/*')
    try:
        latest_file = max(list_of_files, key=os.path.getctime)
    except:
        latest_file = "nofiles"
    return latest_file, list_of_files

def ffmpeger(first_image):
    if first_image == 0:
        print("Sunrise timelapse")
        start_file = "0000"
        folder = "sunrise"
    else:
        print("Sunset timelapse")
        start_file = str(first_image)
        folder = "sunset"
    day = strftime("%d-%b")
    video_filename = f"/home/pi/sunrise2.0/timelapses/{day}-{folder}.mp4"
    push = pb.push_note("Running FFMPEG", "Well done")
    subprocess.call(f"/usr/local/bin/ffmpeg -y -r 30 -f image2 -start_number {start_file} -i /home/pi/sunrise2.0/{folder}/IMAGE_%04d.JPG -vcodec libx264 -preset slow -crf 17 {video_filename}",shell = True)
    scp_copy(video_filename, password, localpath)
    

if __name__ == "__main__":
    running = True
    print("Sun Seeker is monitoring folders for files...")
    while running:
        latest_file, list_of_files = file_most_recent()
        print(latest_file)
        if latest_file == sunrise_watch_file:
            push = pb.push_note("Sunrise Completed", "Ready for the work")
            print("Ding Dong - SUNRISE cooked")
            for i in list_of_files:
                filename = i[27:]
                subprocess.call(f"cp {i} /home/pi/sunrise2.0/sunrise/{filename}", shell=True)
            ffmpeger(0)
            sleep(10)
        elif latest_file == days_end_file:
            push = pb.push_note("Sunset Completed", "Ready for the work")
            print("Ding Dong - SUNSET cooked")
            first_image = fpd-450
            for i in range(450):
                current_filepath = "/home/pi/sunrise2.0/images/IMAGE_" + str(first_image + i) + ".JPG"
                current_filename = "IMAGE_" + str(first_image + i) + ".JPG"
                subprocess.call(f"cp {current_filepath} /home/pi/home/pi/sunrise2.0/sunset/{current_filename}", shell=True)
            ffmpeg_first_number = first_image
            ffmpeger(ffmpeg_first_number)
            running = False
        else:
            print("No luck this time!")
            sleep(4)