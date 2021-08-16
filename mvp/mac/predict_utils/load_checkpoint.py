# Imports python modules
import torch
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


# Function that loads a checkpoint and rebuilds the model
def load_checkpoint(filepath: str) -> torchvision.models:
    """
    Load model from checkpoint file .pth

    Args:
        filepath (str): path to checkpoint file.

    Return:
        torchvision.models: model of neural network
    """
    # Solve problem switching between cuda and cpu device
    if torch.cuda.is_available():
        map_location = lambda storage, loc: storage.cuda()
    else:
        map_location = 'cpu'
    
    # Load checkpoint dict
    checkpoint = torch.load(filepath, map_location=map_location)
    
    # Load model
    model = get_arch(checkpoint['arch'])
        
    for param in model.parameters():
        param.requires_grad = False
        
    model.class_to_idx = checkpoint['class_to_idx']
    model.classifier = checkpoint['classifier']
    model.load_state_dict(checkpoint['model_state_dict'])
        
    return model
