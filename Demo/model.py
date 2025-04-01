import torch
import torch.nn as nn

class NeuralNetwork(nn.Module):
    def __init__(self):
        super(NeuralNetwork, self).__init__()

        # Define image classification layers
        self.image_classification_layer = nn.Sequential(
            nn.Linear(12, 512),
            nn.BatchNorm1d(512),
            nn.ReLU(),
            nn.Dropout(0.50),
            nn.Linear(512, 512)
        )

        # Define final classification layer
        self.final_classification_layer = nn.Sequential(
            nn.Linear(512, 512),
            nn.BatchNorm1d(512),
            nn.ReLU(),
            nn.Dropout(0.50),
            nn.Linear(512, 1),
            nn.Sigmoid()  # Ensure output is between 0 and 1
        )

    def forward(self, x):
        x = x.view(x.size(0), -1)  # Flatten the input tensor
        image_embedding = self.image_classification_layer(x)
        z = torch.cat([image_embedding], 1)
        return self.final_classification_layer(z)

    def predict(self, vector):
        """ Predicts the class label (0 or 1) for a given input vector """
        self.eval()  # Set the model to evaluation mode
        input_tensor = torch.tensor(vector, dtype=torch.float32).unsqueeze(0)  # Add batch dimension
        
        with torch.no_grad():  # No need to compute gradients for inference
            prediction = self(input_tensor)
        
        return 1 if prediction.item() > 0.5 else 0  # Apply threshold

