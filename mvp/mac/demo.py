import logging
import os

import gradio as gr
from torchvision import transforms
import json

from predict_utils.predict import predict
from predict_utils.load_checkpoint import load_checkpoint

logger = logging.getLogger(__name__)

neural_model = None


def demo(image):
    # Image transformation
    image_transform = transforms.Compose([transforms.Resize(255),
                                          transforms.CenterCrop(224),
                                          transforms.ToTensor(),
                                          transforms.Normalize(
                                              [0.485, 0.456, 0.406],
                                              [0.229, 0.224, 0.225])])
    from PIL import Image
    image = Image.fromarray(image)
    image = image_transform(image)
    image.unsqueeze_(0)

    top_p, top_class = predict(image, neural_model, False, 1)

    with open("mvp/mac/tmp/mask_no_mask.json", 'r') as f:
        mask_no_mask = json.load(f)

    result_text = ""
    index = 0
    for elem in top_class:
        mask_state = "yes"
        if "no_mask" in {mask_no_mask[str(int(elem))]}:
            mask_state = "no"
        result_text = f"Mask on face: {mask_state}" + f"\nHow sure I am: {top_p[index] * 100:.0f}%"
        index += 1

    return result_text


if __name__ == "__main__":
    logging.basicConfig(level="DEBUG")

    # Prepare model
    model_dir = 'mvp/mac/tmp/model_checkpoints/checkpoint.pth'
    if not os.path.exists(model_dir):
        raise FileExistsError("Given directory do not exist. Directory: ", model_dir)
    neural_model = load_checkpoint(model_dir)

    # Prepare interface
    iface = gr.Interface(fn=demo, inputs=gr.inputs.Image(shape=(255, 224)), outputs="text")

    # START
    iface.launch(share=True)
