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

    # Argument 1: a path to a image
    parser.add_argument('img_dir', type=str,  # default='data/datasets/train/1/02000_Mask.jpg',
                        help='Path to the image.')

    # Argument 2: a path to a CNN Model Architecture checkpoint
    parser.add_argument('--checkpoint', type=str,  default='model_checkpoints/checkpoint.pth',
                        help='Path to a CNN Model Architecture checkpoint.')

    # Argument 3: a value of K
    parser.add_argument('--top_k', type=int, default=1,
                        help='The value that indicates how many top K should be taken into consideration.')
    
    # Argument 4: a value of learning rate
    parser.add_argument('--category_names', type=str, default='data/dataframe/mask_no_mask.json',
                        help='Path to category names file.')
    
    # Argument 5: a flag for turning on GPU
    parser.add_argument('--gpu', action='store_true', default=False,
                        help='Flag for turning on GPU computing.')

    return parser.parse_args()
