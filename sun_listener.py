# Import Adafruit IO MQTT client.
from Adafruit_IO import MQTTClient
from creds import *
import subprocess # to run file cleanup after the upload
from pushbullet import Pushbullet
from glob import glob
import os
pb = Pushbullet(PUSHBULLET)

def file_most_recent():
    list_of_files = glob('/home/pi/sunrise2.0/images/*')
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file

# Define callback functions which will be called when certain events happen.
def connected(client):
    # calls against it easily.
    print ('Connected to Adafruit IO!  Listening for feed changes...')
    # Subscribe to the three pi-dashboard feeds that will be displayed on the
    # dashboard.  Modify this to subscribe to all the feeds you want to display.
    client.subscribe('button')

def disconnected(client):
    # Disconnected function will be called when the client disconnects.
    print ('Disconnected from Adafruit IO!')
    sys.exit(1)

def message(client, feed_id, payload):
    # Message function will be called when a subscribed feed has a new value.
    # The feed_id parameter identifies the feed, and the payload parameter has
    # the new value.
    print('Feed {0} received new value: {1}'.format(feed_id, payload))
    newest_file = file_most_recent()
    with open(newest_file, "rb") as pic:
        file_data = pb.upload_file(pic, newest_file)
    push = pb.push_file(**file_data)
    #subprocess.call(f"python3 timelapse_request.py", shell=True)

# Create an MQTT client instance.
client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
 
# Setup the callback functions defined above.
client.on_connect    = connected
client.on_disconnect = disconnected
client.on_message    = message
 
# Connect to the Adafruit IO server.
client.connect()
 
# Use the loop_blocking function to run the message loop for processing Adafruit
# IO events.  Since this script doesn't do any other processing this blocking
# version of the message loop is fine.  All the program logic will occur in the
# callback functions above when Adafruit IO feeds are changed.
client.loop_blocking()