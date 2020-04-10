from astral import LocationInfo     # to get the location info `pip3 install astral`
from astral.sun import sun          # to get the sunrise time
from crontab import CronTab
from datetime import datetime, timedelta       

def start_time():
    # set Astral location for Whitley Bay
    city = LocationInfo("Whitley Bay", "England", "Europe/London", 55.0464, -1.4513)
     # get tomorrow's sunrise time
    s = sun(city.observer, date=datetime.date(datetime.now())+timedelta(days=1))
    sunrise_time = s['sunrise']   
    # timelapse shoudl start 1 hour prior
    sunrise = s['sunrise'] + timedelta(minutes=30)
    sunset = s['sunset'] + timedelta(minutes=90)
    day_length = int((sunset - sunrise).total_seconds())
    total_frames = int(day_length/8)
    return sunrise, total_frames

def cron_update(sunrise, total_frames):
    my_cron = CronTab(user='pi')
    my_cron.remove_all(comment='foo')
    job = my_cron.new(command=f'cd /home/pi/sunrise300 && python3 photographer.py {total_frames}', comment='foo')
    job.hour.on(sunrise.hour)
    job.minute.on(sunrise.minute)
    my_cron.write() #write the job to the crontab

if __name__ == "__main__":
    sunrise, total_frames = start_time()
    cron_update(sunrise, total_frames)
    print(f"Fin - Sunrise @ {sunrise}, Total Frames = {total_frames}")