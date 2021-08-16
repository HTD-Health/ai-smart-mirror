# Imports python modules
import torch
import torchvision.models
from torch import optim

# Imports functions created for this program
from train_utils.get_input_args import get_input_args
from train_utils.get_loader import get_directories
from train_utils.get_loader import get_transforms
from train_utils.get_loader import get_datasets


def save_model(model: torchvision.models, optimizer: optim.Adam, save_dir: str) -> None:
    """
    Save model to the .pth file.

    Args:
        model (torchvision.models): model to be saved.
        optimizer (optim.Adam): the way of optimization for model.
        save_dir (str): where and under what name model should be saved.
    """
    # Save the checkpoint 
    dataset = get_datasets(get_directories(get_input_args().data_dir), get_transforms())
    model.class_to_idx = dataset['train'].class_to_idx

    # Define checkpoint with parameters to be saved
    checkpoint = {'input_size': 25088,
                  'output_size': 102, 
                  'classifier': model.classifier,
                  'optimizer': optimizer,
                  'optimizer_state': optimizer.state_dict(),
                  'arch': "vgg16",
                  'class_to_idx': model.class_to_idx,               
                  'model_state_dict': model.state_dict()}

    # Save checkpoint
    torch.save(checkpoint, save_dir)
