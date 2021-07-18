# Imports python modules
import numpy as np
from PIL import Image
from torchvision import transforms


# Process a PIL image for use in a PyTorch model
def process_image(image_path):
    """
    Scales, crops, and normalizes a PIL image for a PyTorch model, returns an Numpy array.
        
    Algorithm:
        image = tf.convert_to_tensor(image)
        image = function to resize image
        image = rehsape the image
        image = image.numpy()
    """
    image = Image.open(image_path)
    image_transform = transforms.Compose([transforms.Resize(255),
                                          transforms.CenterCrop(224),
                                          transforms.ToTensor(),
                                          transforms.Normalize(
                                              [0.485, 0.456, 0.406],
                                              [0.229, 0.224, 0.225])])
    image = image_transform(image)
    image.unsqueeze_(0)
    
    return image
