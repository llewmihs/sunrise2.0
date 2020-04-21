from glob import glob
import subprocess
import os

all_files = sorted(glob("/mnt/myDisk/shared/dayimages/*.JPG"))

for i in all_files:
    if i == "/mnt/myDisk/shared/dayimages/IMAGE_0600.JPG":
        break
    print(f"Copying file {i[-8:]}")
    subprocess.call(f"cp {i} /home/pi/sunrise/IMAGE_{i[-8:]}", shell=True)

subprocess.call("/usr/local/bin/ffmpeg -y -r 30 -f image2 -start_number 0000 -i /home/pi/sunrise//IMAGE_%04d.JPG -vcodec libx264 -preset slow -crf 17 /home/pi/timelapses/17-April-sunrise.mp4", shell=True)

