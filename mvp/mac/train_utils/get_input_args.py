# Imports python modules
import argparse


def get_input_args() -> argparse.Namespace:
    """
    Load variables from command line.

    Return:
        argparse.Namespace: values of the variables packed in Namespace object.
    """
    # Creates Argument Parser object named parser
    parser = argparse.ArgumentParser()

    # Argument 1: a path to a folder
    parser.add_argument('data_dir', type=str,
                        help='Path to the folder of images.')

    # Argument 2: CNN Model Architecture
    parser.add_argument('--arch', type=str, default='vgg16',
                        help='Type of CNN architecture for model.')

    # Argument 3: a path to a neural network save file
    parser.add_argument('--save_dir', type=str, default='model_checkpoints/checkpoint.pth',
                        help='Path to the folder where save model checkpoint.')
    
    # Argument 4: a value of learning rate
    parser.add_argument('--learning_rate', type=float, default=0.01,
                        help='Value of learning rate for model.')
    
    # Argument 5: a number of hidden units in hidden layers
    parser.add_argument('--hidden_units', type=int, default=512,
                        help='Number of hidden units in model.')
    
    # Argument 6: a number of epochs
    parser.add_argument('--epochs', type=int, default=1,
                        help='Number of epochs for training model.')
    
    # Argument 7: a flag for turning on GPU
    parser.add_argument('--gpu', action='store_true', default=False,
                        help='Flag for turning on GPU computing.')

    return parser.parse_args()
