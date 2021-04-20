import src.model.ai_mask_model.mask_detector.mask_classifier as model


def model_loader(path: str):
    """
    Load model from checkpoint file.

    Parameters:
        path (str): path to saved checkpoint model.

    Return:
        trained model based on saved model file with all trained weights.
    """
    return model.MaskClassifier.load_from_checkpoint(path)
