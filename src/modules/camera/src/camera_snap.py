import time
from datetime import datetime

import picamera

from src.utils.config_loader import load_config_file


def camera_snap() -> str:
    # Load configuration data
    config_data = load_config_file()
    weight = config_data["camera"]["functionality"]["resolution"]["weight"]
    height = config_data["camera"]["functionality"]["resolution"]["height"]
    image_format = config_data["camera"]["functionality"]["image_format"]

    with picamera.PiCamera() as camera:
        camera.resolution = (weight, height)
        camera.start_preview()

        # Camera warm-up time
        time.sleep(2)

        # Prepare file name
        now = datetime.now()
        now_str = now.strftime("%d%m%Y%H%M%S")
        snap_name = now_str + image_format

        # Take snap
        camera.capture(snap_name)

        return snap_name
