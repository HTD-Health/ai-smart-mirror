import time
from datetime import datetime

import picamera

# TODO: add setting things up (in function?)
# TODO: load config from file
camera_resolution_weight = 1024
camera_resolution_height = 768
image_format = ".jpg"
# TODO: add setting consumer
# TODO: add setting producer
# TODO: adding waiting for signal to work

with picamera.PiCamera() as camera:
    camera.resolution = (camera_resolution_weight, camera_resolution_height)
    camera.start_preview()

    # Camera warm-up time
    time.sleep(2)

    # Prepare file name
    now = datetime.now()
    now_str = now.strftime("%d%m%Y%H%M%S")
    snap_name = now_str + image_format

    # Take snap
    camera.capture(snap_name)

# TODO: adding sending pic
