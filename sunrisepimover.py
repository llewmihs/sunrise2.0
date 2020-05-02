from subprocess import call
from time import strftime


root_folders = "/mnt/sunrise_storage/shared/"
main_folder = root_folders + "dayimages"
store_folder = strftime(f"{root_folders}%d-%B-%Y")

call(f"mv {main_folder} {store_folder}", shell=True)
call(f"mkdir {main_folder}", shell=True)
