# this file is triggered when the user sends a message via IFTTT and Adafruit IO
# It picks up the current file number, and then works out , 300 before it, then waits til 300 after
# This set of images is then copied to another folder and then ffmpeg converts it into a timelapse
# The user, having seen a "nice cloud formation", now can see how it got there and where it's going next

# what modules do we need?
from glob import glob # this allows us to get the files from a folder
import os # os module will help glob to check for the newest file
import subprocess # this will allow us to call copy, and fmmpeg commands from the terminal

# set the folder path to watch
watch_folder = "/home/pi/sunrise2.0/images/"      # this is for the Pi Version
watch_folder = ""

# define a function to calculate the start and end files
def edge_finder(watch_folder):
    all_files = glob(watch_folder+"*.JPG")  #create a list containing all JPG files
    latest_file = max(all_files, key=os.path.getctime)  # find the most recent file
    # take the final 4 digits of the filenumber
    # latest_file_num = latest_file[27:-4]      # this is for the Pi Version
    latest_file_num = latest_file[6:-4]
    # subtrack 300 files from the current number
    first_image = int(latest_file_num)-300
    last_image = first_image + 600
    first_file_name = f"{watch_folder}IMAGE_{first_image:04d}.JPG" 
    final_file_name = f"{watch_folder}IMAGE_{last_image:04d}.JPG"
    return first_file_name, final_file_name

def file_waiter(final_file_name, watch_folder):
    searching = True
    while searching:
        all_files = glob(watch_folder+"*.JPG")
        latest_file = max(all_files, key=os.path.getctime)
        if latest_file == final_file_name:

def copy_images(first_image_num, last_image_num):
    for i in range(first_image_num,last_image_num+1):
        copy_file = 

if __name__ == "__main__":
