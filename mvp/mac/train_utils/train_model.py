# Imports python modules
import torch
import torchvision.models
from torch import nn
from torch import optim
from datetime import datetime
from loguru import logger


def train_model(
        model: torchvision.models,
        loader: dict,
        gpu: bool,
        learning_rate: float,
        epochs: int
) -> (torchvision.models, optim.Adam):
    """
    Train model.

    Args:
        model (torchvision.models): torchvision model of neural network.
        loader (dict): dictionary containing object of datasets loaders.
        gpu (bool): flag to turn of/on calculations on GPU.
        learning_rate (float): learning rate for learning process.
        epochs (int): number of epochs for learning process.
    """
    # ---
    # INIT MODEL
    # ---
    # Freeze parameters so we don't backpropagation through them
    for param in model.parameters():
        param.requires_grad = True
        
    if gpu:
        # Use GPU if it's available
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    else:
        device = "cpu"
    model.to(device)
        
    # Setup loss function
    criterion = nn.NLLLoss()

    # Setup optimizer. Only train the classifier parameters, feature parameters are frozen
    optimizer = optim.Adam(model.classifier.parameters(), lr=learning_rate)
    
    # ---
    # MODEL LEARNING PROCESS
    # ---
    # How many times we repeat the process
    steps = 0
    running_loss = 0
    print_every = 5
    train_losses = []
    valid_losses = []

    # Training loop
    for epoch in range(epochs):
        # For each image in data set, train neural network model
        for inputs, labels in loader['train']:
            steps += 1
            # Move input and label tensors to the default device
            inputs, labels = inputs.to(device), labels.to(device)

            # Calculating predicted output
            output = model.forward(inputs)
            # Calculating loss
            loss = criterion(output, labels)

            # Training pass
            optimizer.zero_grad()
            # Calculating backpropagation based on loss
            loss.backward()
            # Update weights and biases
            optimizer.step()

            # Calculating loss for epoch
            running_loss += loss.item()

            # For each print_every (default 5) images calculate validation
            if steps % print_every == 0:
                # Initiate value of test loss after each epoch
                valid_loss = 0
                # Initiate value of accuracy after each epoch
                accuracy = 0
                # Turn off gradients for validation to save memory and computations
                with torch.no_grad():
                    # Turn on model evaluation mode to turn off dropout
                    model.eval()
                    for inputs, labels in loader['valid']:
                        # Move input and label tensors to the default device
                        inputs, labels = inputs.to(device), labels.to(device)
                        # Calculating test predicted output
                        output = model.forward(inputs)
                        # Calculating loss
                        batch_loss = criterion(output, labels)

                        # Calculate accuracy
                        # ---
                        # Get class probability
                        output_class_probability = torch.exp(output)
                        # Get top highest values of probability for classes
                        top_p, top_class = output_class_probability.topk(1, dim=1)
                        # Calculate if classes are correct
                        equals = top_class == labels.view(*top_class.shape)
                        # Calculating accuracy
                        accuracy += torch.mean(equals.type(torch.FloatTensor)).item()

                        # Calculating test loss for epoch
                        valid_loss += batch_loss.item()

                # Turn off evaluation mode and turn on training mode aka turn on dropout
                model.train()

                # Add train loss for epoch
                train_losses.append(running_loss/len(loader['train']))
                # Add validation loss for epoch
                valid_losses.append(valid_loss/len(loader['valid']))

                # Print recaption after epoch
                step_time = datetime.now().strftime("%H:%M:%S")
                logger.info(f"{step_time}: "                            
                            f"Epoch {epoch+1}/{epochs}.. "
                            f"Train loss: {running_loss/print_every:.3f} ; "
                            f"Validation loss: {valid_loss/len(loader['valid']):.3f}.. "
                            f"Validation accuracy: {accuracy/len(loader['valid']):.3f}")
                    
                # Initiate value of loss for each print_every (default 5) image
                running_loss = 0
                    
    return model, optimizer
