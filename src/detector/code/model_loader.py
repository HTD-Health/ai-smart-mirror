from mask_detector.mask_classifier import MaskClassifier
from mask_detector.models.mobile_net_v2 import MobileNetV2


def model_loader(path: str):
    """
    Load model from checkpoint file.

    Parameters:
        path (str): path to saved checkpoint model.

    Return:
        trained model based on saved model file with all trained weights.
    """
    net = MobileNetV2()
    return MaskClassifier.load_from_checkpoint(path, net=net)
