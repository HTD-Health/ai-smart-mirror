import logging
import time
import os

from camera import ActiveCamera
from camera import make_snap
from predict_utils.predict import predict
from predict_utils.print_results import print_results
from predict_utils.load_checkpoint import load_checkpoint
from predict_utils.process_image import process_image

logger = logging.getLogger(__name__)


def run(image_width: int, image_height: int, image_format: str, snap_directory: str, neural_model: object):
    # Turn on camera
    camera = ActiveCamera(
        width=image_width,
        height=image_height,
    )

    # Taking a picture
    snap_name = make_snap(camera, image_format, snap_directory)
    logger.debug(f'Snap at directory: {snap_name}')
    time.sleep(3)

    # Detect mask
    image = process_image(snap_directory + snap_name)
    top_p, top_class = predict(image, neural_model, False, 1)

    # Print class and a probability
    print_results(top_p, top_class, "src/tmp/mask_no_mask.json")

    # Clean up
    os.remove(snap_directory + snap_name)

    # To not spam with measurements, wait until renewing the whole process
    time.sleep(10)


if __name__ == "__main__":
    # PREPARATION
    logging.basicConfig(level="DEBUG")

    # Prepare camera
    image_width = 1024
    image_height = 768
    image_format = 'jpg'

    # Prepare model
    model_dir = 'src/tmp/model_checkpoints/checkpoint.pth'
    if not os.path.exists(model_dir):
        raise FileExistsError("Given directory do not exist. Directory: ", model_dir)
    neural_model = load_checkpoint(model_dir)

    # Prepare image destination
    image_dir = 'src/tmp/images/'
    if not os.path.exists(image_dir):
        raise FileExistsError("Given directory do not exist. Directory: ", image_dir)

    # START
    while True:
        run(image_width, image_height, image_format, image_dir, neural_model)
