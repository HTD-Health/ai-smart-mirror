# Imports python modules
import torch.nn.functional as f
from torch import nn


class Classifier(nn.Module):
    """
    Rule of thumb during building neural network:
    * The number of hidden neurons should be between the size of the input layer and the size of the output layer.
    * The number of hidden neurons should be 2/3 the size of the input layer, plus the size of the output layer.
    * The number of hidden neurons should be less than twice the size of the input layer.
    """

    def __init__(self, hidden_units):
        super().__init__()
        self.fc1 = nn.Linear(25088, hidden_units)  # First layer as input get 25088 pixels
        self.fc2 = nn.Linear(hidden_units, 102)  # Output layer give as output 102 classes with probabilities for each

        # Dropout model with 0.2 drop probability
        self.dropout = nn.Dropout(p=0.2)

    def forward(self, x):
        """
        TODO: write docstring
        """
        # Make sure input tensor is flattened
        x = x.view(x.shape[0], -1)

        x = self.dropout(f.relu(self.fc1(x)))  # First layer activation function is ReLU (is quick) with dropout

        # Output so no dropout
        x = f.log_softmax(self.fc2(x), dim=1)

        return x


def get_classifier(hidden_units: int) -> Classifier:
    """
    Create classifier object.

    Args:
        hidden_units (int): number of hidden layer outputs

    Return:
        Classifier: classifier object determine number of layers, activation function and forward function.
    """
    # Build neural network classifier     
    return Classifier(hidden_units)
