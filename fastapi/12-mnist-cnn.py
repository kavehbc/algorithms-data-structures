from typing import Annotated, Union
from fastapi import FastAPI, Path, Query, UploadFile, File
import uvicorn
import pickle
import numpy as np
from PIL import Image
from torchvision import transforms
import torch
from torch import nn
import torch.nn.functional as F
import io


app = FastAPI(title="MNIST Classifier")

class Network(nn.Module):
    def __init__(self):
        super(Network, self).__init__()
        self.convolutional_neural_network_layers = nn.Sequential(
            nn.Conv2d(in_channels=1, out_channels=12, kernel_size=3, padding=1, stride=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2),
            nn.Conv2d(in_channels=12, out_channels=24, kernel_size=3, padding=1, stride=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2)
        )
        self.linear_layers = nn.Sequential(
            nn.Linear(24 * 7 * 7, out_features=64),
            nn.ReLU(),
            nn.Dropout(p=0.2),
            nn.Linear(in_features=64, out_features=10)
        )
    def forward(self, x):
        x = self.convolutional_neural_network_layers(x)
        x = x.view(x.size(0), -1)
        x = self.linear_layers(x)
        x = F.log_softmax(x, dim=1)
        return x
    

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/mnist")
async def mnist_classification(file: UploadFile):
    """
    
    """
    
    model = torch.load("../objects/pytorch_mnist_cnn_model.pkl", map_location=torch.device('cpu'))
    
    # with open("../data/mnist_sample/1.png", "rb") as image_file:
    #     image_bytes = io.BytesIO(image_file.read())
    
    request_object_content = await file.read()
    image = Image.open(io.BytesIO(request_object_content))

    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1,), (0.3,))
    ])
    img_tranform = transform(image)
    img = img_tranform
    img = img.view(-1, 1, 28, 28)
    with torch.no_grad():
        logits = model.forward(img)

    probabilities = F.softmax(logits, dim=1).detach().cpu().numpy().squeeze()

    value = int(np.where(probabilities == probabilities.max())[0][0])

    return {"prediction":value}


if __name__ == "__main__":
    uvicorn.run("12-mnist-cnn:app",
                host='127.0.0.1',
                port=8000,
                reload=True)
