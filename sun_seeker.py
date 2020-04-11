# this file monitors the file names of the image taken throughout the day
# on two occasions it triggers a ffmepg to create a timelapse

import subprocess
from glob import glob
from sunny_conf import fpd
from time import sleep, strftime
import os

sunrise_watch_file = '/home/pi/sunrise2.0/images/IMAGE_0449.JPG'
days_end_file = '/home/pi/sunrise2.0/images/end.txt'

# sunset start file
def sunset_start(fpd):
    file_num = "/home/pi/sunrise2.0/images/IMAGE_" + str(fpd-450) + ".JPG"
    return file_num

def file_most_recent():
    list_of_files = glob('/home/pi/sunrise2.0/images/*.JPG')
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file, list_of_files

def ffmpeger(first_image):
    if first_image == 0:
        print("Sunrise timelapse")
        start_file = "0000"
        folder = "sunrise"
    else:
        print("Sunset timelapes")
        start_file = str(first_image)
        folder = "sunset"
    day = strftime("%d-%b")
    video_filename = f"/home/pi/sunrise2.0/timelapses/{day}-{folder}.mp4"
    subprocess.call(f"/usr/local/bin/ffmpeg -y -r 30 -f image2 -start_number {start_file} -i /home/pi/sunrise2.0/{folder}/IMAGE_%04d.JPG -vcodec libx264 -preset slow -crf 17 {video_filename}",shell = True)
    

if __name__ == "__main__":
    running = True
    print("Sun Seeker is monitoring folders for files...")
    while running:
        latest_file, list_of_files = file_most_recent()
        if latest_file == sunrise_watch_file:
            print("Ding Dong - SUNRISE cooked")
            for i in list_of_files:
                filename = i[27:]
                subprocess.call(f"cp {i} /home/pi/sunrise2.0/sunrise/{filename}", shell=True)
            ffmpeger(0)
        elif latest_file == days_end_file:
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