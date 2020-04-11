# file to create the sunrise and sunset timelapses
# monitors a folder for points at which to start timelapsing
from glob import glob
import os
from time import sleep, strftime
import subprocess

sunrise_watch_file = "IMAGE_1000.JPG" # this is the final file of the sunrise

def file_most_recent():
    list_of_files = glob('/home/pi/sunrise2.0/images/*.JPG')
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file, list_of_files

if __name__ == "__main__":
    running = True
    print("Running")
    while running:
        latest_file, list_of_files = file_most_recent()
        if latest_file == sunrise_watch_file:
            print("Ding Dong")
            # move the files into a new folder:
            for i in list_of_files:
                filename = i[27:]
                subprocess.call(f"cp {i} /home/pi/sunrise2.0/sunrises/{filename}") ### what is i??
            # run ffmpeg to create the video file
            video_filename = strftime("%d-%b-sunrise.mp4")
            subprocess.call(f"/usr/local/bin/ffmpeg -y -r 30 -f image2 -start_number 0000 -i /home/pi/sunrise2.0/sunrises/IMAGE_%04d.JPG -vcodec libx264 -preset slow -crf 17 {video_filename}",shell = True)
            running = False
        else:
            print("Nah.")
            sleep(5)
    print("End of games")
            

