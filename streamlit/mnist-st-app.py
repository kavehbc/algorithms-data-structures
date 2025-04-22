import streamlit as st
import keras
from PIL import Image
import numpy as np
import io

def main():
    model = keras.models.load_model("mnist/MNIST_keras_CNN.h5")

    st.title("MNIST Classifier")
    uploaded_file = st.file_uploader("Upload your image", type=["jpg", "png"])
    if uploaded_file is not None:
        data = uploaded_file.getvalue()
        img = Image.open(io.BytesIO(data)).resize((28, 28))
        st.image(img)

        arr = np.array(img)
        
        # arr = np.average(arr, axis=-1)
        arr = arr.reshape(1, 28, 28, 1)
        prediction = model.predict(arr)
        prediction = np.argmax(prediction)
        st.subheader(prediction)
        
if __name__ == "__main__":
    main()