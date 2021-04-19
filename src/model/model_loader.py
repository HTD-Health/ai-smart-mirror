import ... as smart_mirror_model  # TODO: figure out how to manage exporting MM repo to import it here

def model_loader(path: str):
    """
    Load model from checkpoint file.

    Parameters:
        path (str): path to saved checkpoint model.

    Return:
        trained model based on saved model file with all trained weights.
    """
    return smart_mirror_model.load_from_checkpoint(path)
