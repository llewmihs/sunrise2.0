from picamera import PiCamera
import sys

# the Picamera
camera = PiCamera()
camera.resolution = (3280, 2464)

if len(sys.argv) > 1:
    number_of_snaps = int(sys.argv[1])
else:
    print("No additional arguments, exiting")
    exit

def the_camera(no_of_frames, delay=8):
    camera.start_preview()
    sleep(2) # Camera warm-up time
    for i in range(no_of_frames):
        file_path = "/home/pi/sunrise2.0/images/" + 'IMAGE_' '{0:04d}'.format(i)+".JPG"
        camera.capture(file_path)
        sleep(delay)

if __name__ == "__main__":
    print(f"Staring to take {number_of_snaps} photos!")
    the_camera(number_of_snaps)
    print("Finished")

    



