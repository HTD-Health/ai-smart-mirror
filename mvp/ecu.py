import logging
import time
import os

from distance_sensor import measure_distance
from distance_sensor import DistanceSensor
from camera import ActiveCamera
from camera import make_snap
from detector import detect_mask
from detector import model_loader

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    # PREPARATION
    logging.basicConfig(level="DEBUG")

    # Prepare distance sensor
    trigger_pin = 7
    echo_pin = 11
    sleep_time = 0.1
    sensor_settle_time = 0.3
    threshold_distance = 80

    distance_sensor = DistanceSensor(trigger_pin, echo_pin)
    time.sleep(sensor_settle_time)  # Allow module to settle

    # Prepare camera
    image_width = 1024
    image_height = 768
    image_format = 'jpg'
    pic_directory = '/tmp/'
    snap_name_container = ['']

    camera = ActiveCamera(
        width=image_width,
        height=image_height,
    )

    # Prepare model
    model_dir = 'tmp/models/epoch=16-step=8499.ckpt'
    # Check if model directory exist
    if not os.path.exists(model_dir):
        raise FileExistsError("Given directory do not exist. Directory: ", model_dir)

    image_dir = 'tmp/images/'
    # Check if image directory exist
    if not os.path.exists(image_dir):
        raise FileExistsError("Given directory do not exist. Directory: ", image_dir)
    # Load model
    neural_model = model_loader(model_dir)

    # START
    while True:
        # Measure distance
        distance = measure_distance(distance_sensor)

        if distance < threshold_distance:
            logger.debug(f'Received distance: {distance} cm')

            # Taking a picture
            snap_name = make_snap(camera, image_format, pic_directory)
            logger.debug(f'Snap at directory: {snap_name} cm')
            print(f'Camera took snap at: {snap_name}')

            # Detect mask
            detect_mask(snap_name, neural_model)

            # To not spam with measurements, wait until renewing the whole process
            time.sleep(6)
