from fastapi import FastAPI, UploadFile
from fastapi.responses import HTMLResponse
import uvicorn
import keras
from PIL import Image
import numpy as np
import io

app = FastAPI(title="MNIST API")

@app.get("/")
def homepage():
    html = """
        <html><head><title>MNIST API</title></head>
        <body><h1>MNIST API</h1></body>
        </html>
    """
    return HTMLResponse(content=html, status_code=200)

@app.post("/image")
async def classify(image: UploadFile):
    data = image.file.read()
    model = keras.models.load_model("mnist/MNIST_keras_CNN.h5")

    img = Image.open(io.BytesIO(data)).resize((28, 28))

    arr = np.array(img)

    if len(arr.shape) == 3:
        arr = np.average(arr, axis=-1)
        
    arr = arr.reshape(1, 28, 28, 1)
    prediction = model.predict(arr)
    prediction = int(np.argmax(prediction))
    return {"class": prediction}

if __name__ == "__main__":
    uvicorn.run("mnist-api:app",
                host="0.0.0.0",
                port=8000,
                reload=True)