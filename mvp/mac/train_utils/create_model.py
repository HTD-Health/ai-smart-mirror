# Imports python modules
import torchvision.models

# Imports functions created for this program
from train_utils.get_arch import get_arch
from train_utils.get_classifier import get_classifier


def create_model(arch: str, hidden_units: int) -> torchvision.models:
    """
    Create a model based on passed architecture with custom classifier.

    Args:
        arch (str): name of architecture.
        hidden_units (int): number of hidden layer outputs

    Return:
        torchvision.models: classifier model
    """
    # Load pre-trained model based on selected architecture
    model = get_arch(arch)
        
    # Create own classifier
    model.classifier = get_classifier(hidden_units)
    
    return model
