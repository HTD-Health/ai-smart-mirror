# Imports python modules
import torchvision.models


def get_arch(arch: str) -> torchvision.models:
    """
    Return object of the network architecture from torchvision library.

    Args:
        arch (str): name of architecture.

    Return:
        torchvision.models: object of the proper architecture class.
    """
    if arch == 'resnet18':
        model = torchvision.models.resnet18(pretrained=True)
    if arch == 'alexnet':
        model = torchvision.models.alexnet(pretrained=True)
    if arch == 'vgg13':
        model = torchvision.models.vgg13(pretrained=True)
    if arch == 'vgg16':    
        model = torchvision.models.vgg16(pretrained=True)
    
    return model
