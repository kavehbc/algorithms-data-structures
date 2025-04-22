import streamlit as st
from PIL import Image
import numpy as np
from torchvision import transforms
import torch
from torch import nn
import torch.nn.functional as F
import io


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
def main():
    st.write("MNIST CNN Classifier")

    model = torch.load("Torch_cnn_model.pkl", map_location=torch.device('cpu'))

    uploaded_file = st.file_uploader("Choose a file")

    # If user attempts to upload a file.
    if uploaded_file is not None:

        image_bytes = io.BytesIO(uploaded_file.read())
        # Show the image filename and image.
        st.write(f'filename: {uploaded_file.name}')
        st.image(image_bytes)

        # image_path = 'images/5.jpeg'
        # image = Image.open(image_path)

        image = Image.open(image_bytes)
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

        value = np.where(probabilities == probabilities.max())[0][0]
        st.subheader(value)


if __name__ == "__main__":
    main()