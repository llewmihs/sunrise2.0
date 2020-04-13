# this file is triggered when the user sends a message via IFTTT and Adafruit IO
# It picks up the current file number, and then works out , 300 before it, then waits til 300 after
# This set of images is then copied to another folder and then ffmpeg converts it into a timelapse
# The user, having seen a "nice cloud formation", now can see how it got there and where it's going next

# what modules do we need?
from glob import glob # this allows us to get the files from a folder
import os # os module will help glob to check for the newest file
import subprocess # this will allow us to call copy, and fmmpeg commands from the terminal
from time import sleep, strftime

# set the folder path to watch
watch_folder = "/home/pi/sunrise2.0/images/"      # this is for the Pi Version
#watch_folder = ""

# define a function to calculate the start and end files
def edge_finder(watch_folder):
    all_files = glob(watch_folder+"*.JPG")  #create a list containing all JPG files
    latest_file = max(all_files, key=os.path.getctime)  # find the most recent file
    # take the final 4 digits of the filenumber
    latest_file_num = latest_file[27:-4]      # this is for the Pi Version
    #latest_file_num = latest_file[6:-4]
    # subtrack 300 files from the current number
    first_image = int(latest_file_num)-300
    last_image = first_image + 600
    first_file_name = f"{watch_folder}IMAGE_{first_image:04d}.JPG" 
    final_file_name = f"{watch_folder}IMAGE_{last_image:04d}.JPG"
    print(first_file_name)
    print(final_file_name)
    return first_file_name, final_file_name, first_image, last_image

def file_waiter(final_file_name, watch_folder):
    searching = True
    while searching:
        print("."),
        all_files = glob(watch_folder+"*.JPG")
        latest_file = max(all_files, key=os.path.getctime)
        if latest_file == final_file_name:
            searching = False
        sleep(4)
    print("File found")
    
def copy_images(watch_folder, first_image_num, last_image_num):
    for i in range(first_image_num,last_image_num+1):
        copy_instruction = f"cp {watch_folder}IMAGE_{i:04d}.JPG /home/pi/sunrise2.0/userlapse/IMAGE_{i:04d}.JPG"
        subprocess.call(f"{copy_instruction}", shell=True)

def ffmpeg(first_image_num, lapse_folder = "/home/pi/sunrise2.0/timelapses/"):
    filename = strftime("%d-%b-%h-%M timelapse.mp4")
    subprocess.call(f"/usr/local/bin/ffmpeg -y -r 30 -f image2 -start_number {first_image_num::04d} -i /home/pi/sunrise2.0/userlapse/IMAGE_%04d.JPG -vcodec libx264 -preset slow -crf 17 {lapse_folder}{filename}",shell = True)

if __name__ == "__main__":
    first_file_name, final_file_name, first_num, final_num = edge_finder(watch_folder)
    file_waiter(final_file_name, watch_folder)
    copy_images(watch_folder,first_num, final_num)
    ffmpeg(first_num)

