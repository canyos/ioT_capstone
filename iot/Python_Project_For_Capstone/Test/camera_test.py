from picamera2 import Picamera2, Preview
import time

picam2 = Picamera2()
camera_config = picam2.create_still_configuration(main={"size": (1920, 1080)}, lores={"size": (640, 480)}, display="lores")
picam2.configure(camera_config)
#picam2.start_preview(Preview.QTGL)
picam2.start()
index = 0
while True:
	image_name = str(index) + ".jpg"
	picam2.capture_file(image_name)
	index += 1
	if index == 12:
		index = 0
	time.sleep(2)
	
