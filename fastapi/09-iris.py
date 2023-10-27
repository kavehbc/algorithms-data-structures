from typing import Annotated, Union
from fastapi import FastAPI, Path, Query
import pickle
import pandas as pd
import base64

app = FastAPI(title="Iris Classifier")


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/test/{test_id}")
def read_item(test_id: int, q: str = None):
    return {"test_id": test_id, "q": q}

@app.get("/iris/model")
def download_model():
    """
    Download pickle object of the Neural Network model
    """
    with open("../objects/iris-nn.pkl", "rb") as model:
        encodedZip = base64.b64encode(model.read())
    
    return {"extension": ".pkl", "model": encodedZip}

@app.get("/iris")
def iris_classification(petal_length: float = Query(description="Length of Petal", default=5, ge=1, le=6.9),
                        petal_width: float = Query(description="Width of Petal", default=2, ge=0.1, le=2.5),
                        sepal_length: float = Query(description="Length of Sepal", default=5.3, ge=4.3, le=7.9),
                        sepal_width: float = Query(description="Width of Sepal", default=4, ge=2, le=4.4)):
    """
    This is the classification on IRIS dataset
    
    :param: petal_length
    :param: petal_width
    :param: sepal_length
    :param: sepal_width
    
    example: http://127.0.0.1:8000/iris?petal_length=5&petal_width=2&sepal_length=5.3&sepal_width=4
    
    """
    
    scaler = pickle.load(open("../objects/iris-scaler.pkl", "rb"))
    model = pickle.load(open("../objects/iris-nn.pkl", "rb"))

    columns_to_scale = ['sepal length (cm)', 'sepal width (cm)',
                        'petal length (cm)', 'petal width (cm)']

    df = pd.DataFrame([[sepal_length, sepal_width, petal_length, petal_width]],
                      columns=columns_to_scale)

    df[columns_to_scale] = scaler.transform(df[columns_to_scale])

    prediction = model.predict(df) # ndArray
    prediction = int(prediction[0]) # to serialize the result

    species_name = ['setosa', 'versicolor','virginica']
    
    return {"prediction":
                {'species': prediction,
                 'name': species_name[prediction]}
           }


if __name__ == "__main__":
    uvicorn.run("09-iris:app",
                host='127.0.0.1',
                port=8000,
                reload=True)
