# Imports python modules
import torch
from torchvision import transforms
from torchvision import datasets


def get_directories(data_dir: str) -> dict:
    """
    Create directories to folders containing train, validation and tests data.

    Args:
        data_dir(str): dictionary for root folder.

    Return:
        dict: dictionary of directories for train, validation and test data.
    """
    train_dir = data_dir + '/train'
    valid_dir = data_dir + '/valid'
    test_dir = data_dir + '/test'    
    
    return {'train': train_dir, 'valid': valid_dir, 'test': test_dir}


def get_transforms() -> dict:
    """
    Create functions for transforming training, validation and test data.

    Return:
        dict: dictionary of transformation function for train, validation and test data.
    """
    train_transform = transforms.Compose([transforms.RandomRotation(30),
                                       transforms.RandomResizedCrop(224),
                                       transforms.RandomHorizontalFlip(),
                                       transforms.ToTensor(),
                                       transforms.Normalize([0.485, 0.456, 0.406],
                                                            [0.229, 0.224, 0.225])])
    valid_transform = transforms.Compose([transforms.Resize(255),
                                          transforms.CenterCrop(224),
                                          transforms.ToTensor(),
                                          transforms.Normalize([0.485, 0.456, 0.406],
                                                               [0.229, 0.224, 0.225])])
    test_transform = transforms.Compose([transforms.Resize(255),
                                          transforms.CenterCrop(224),
                                          transforms.ToTensor(),
                                          transforms.Normalize([0.485, 0.456, 0.406],
                                                               [0.229, 0.224, 0.225])])
    
    return {'train': train_transform, 'valid': valid_transform, 'test': test_transform}


def get_datasets(directories: dict, transforms: dict) -> dict:
    """
    Create datasets for  training, validation and test data.

    Args:
        directories (dict): directories for train, validation and test data.
        transforms (dict): functions to transforms incoming data to datasets.

    Return:
        dict: dictionary of train, validation and test datasets.
    """
    train_dataset = datasets.ImageFolder(directories['train'], transform=transforms['train'])
    valid_dataset = datasets.ImageFolder(directories['valid'], transform=transforms['valid'])
    test_dataset = datasets.ImageFolder(directories['test'], transform=transforms['test'])

    return {'train': train_dataset, 'valid': valid_dataset, 'test': test_dataset}


def get_loader(data_dir: str) -> dict:
    """
    Create data loaders functions for train, validation and test data.

    Args:
        data_dir(str): dictionary for root folder.

    Return:
        dict: dictionary of data loaders for train, validation and test datasets.
    """
    # Create directories based on passed path
    directories = get_directories(data_dir)
    
    # Defined of transforms for the training, validation and testing sets
    transforms = get_transforms()
    
    # Load the datasets with ImageFolder for train set
    datasets = get_datasets(directories, transforms)
    
    # Defined the dataloaders, using the image datasets and the trainforms
    train_loader = torch.utils.data.DataLoader(datasets['train'], batch_size=64, shuffle=True)
    valid_loader = torch.utils.data.DataLoader(datasets['valid'], batch_size=32)
    test_loader = torch.utils.data.DataLoader(datasets['test'], batch_size=32)
    
    return {'train': train_loader, 'valid': valid_loader, 'test': test_loader}
