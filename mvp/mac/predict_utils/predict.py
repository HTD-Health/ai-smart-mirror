# Imports python modules
import torch


# Predict the class from an image file
def predict(image, model, gpu, top_k=5):
    """Predict the class (or classes) of an image using a trained deep learning model."""
    if gpu:        
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    else:
        device = "cpu"
    model.to(device)
    
    top_p, top_class = torch.exp(model.forward(image)).topk(top_k, dim=1)
    
    return top_p[0], top_class[0]
