import logging
import os

import gradio as gr
from torchvision import transforms

from predict_utils.predict import predict
from predict_utils.print_results import print_results
from predict_utils.load_checkpoint import load_checkpoint


logger = logging.getLogger(__name__)


def demo(image):
    # Prepare model
    model_dir = 'src/tmp/model_checkpoints/checkpoint.pth'
    if not os.path.exists(model_dir):
        raise FileExistsError("Given directory do not exist. Directory: ", model_dir)
    neural_model = load_checkpoint(model_dir)

    image_transform = transforms.Compose([transforms.Resize(255),
                                          transforms.CenterCrop(224),
                                          transforms.ToTensor(),
                                          transforms.Normalize(
                                              [0.485, 0.456, 0.406],
                                              [0.229, 0.224, 0.225])])
    image = image_transform(image)
    image.unsqueeze_(0)

    top_p, top_class = predict(image, neural_model, False, 1)
    return print_results(top_p, top_class, "src/tmp/mask_no_mask.json")


if __name__ == "__main__":
    # PREPARATION
    logging.basicConfig(level="DEBUG")

    # Prepare camera
    image_width = 1024
    image_height = 768
    image_format = 'jpg'

    # Prepare image destination
    iface = gr.Interface(fn=demo, inputs=gr.inputs.Image(shape=(200, 200)), oututs="text")

    # START
    iface.launch()
