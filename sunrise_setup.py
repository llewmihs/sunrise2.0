# sunrise_setup is called daily by the cron
# it calculate the length of the time lapse (sunrise - 40 mins to sunset + 2 minutes)
# it returns the number of frame that will be taken in a  given day to the file sunny_conf.py
# it then write to the crontab to launch the camera at the correct ime, 40 minutes before the sunirse

from astral import LocationInfo     # to get the location info `pip3 install astral`
from astral.sun import sun          # to get the sunrise time
from crontab import CronTab
from datetime import datetime, timedelta
import subprocess   
from creds import *
from pushbullet import Pushbullet   # notification software to monitor the programme remotely `pip3 install pushbullet.py`
pb = Pushbullet(PUSHBULLET)

def start_time():
    # set Astral location for Whitley Bay
    city = LocationInfo("Whitley Bay", "England", "Europe/London", 55.0464, -1.4513)
     # get tomorrow's sunrise time
    s = sun(city.observer, date=datetime.date(datetime.now()))
    # timelapse shoudl start 1 hour prior
    sunrise = s['sunrise']
    sunset = s['sunset'] + timedelta(minutes=30)
    day_length = int((sunset - sunrise).total_seconds())
    total_frames = int(day_length/8)
    return sunrise, total_frames

def update(sunrise, total_frames):
    my_cron = CronTab(user='pi')
    my_cron.remove_all(comment='bar')
    job = my_cron.new(command=f'cd /home/pi/sunrise2.0 && python3 photographer.py', comment='bar')
    job.hour.on(sunrise.hour)
    job.minute.on(sunrise.minute)
    my_cron.write() #write the job to the crontab
    #delete the previous day's config file
    subprocess.call("rm -r sunny_conf.py", shell=True)
    subprocess.call(f"echo fpd=900>> sunny_conf.py", shell=True)


if __name__ == "__main__":
    sunrise, total_frames = start_time()
    update(sunrise, total_frames)
    push = pb.push_note("Setup Complete", f"Total frames: {total_frames}. Time: {sunrise}.")
    print(f"Fin - Sunrise @ {sunrise}, Total Frames = {total_frames}")