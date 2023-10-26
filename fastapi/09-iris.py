from fastapi import FastAPI
import uvicorn
import pickle
import pandas as pd

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/test/{test_id}")
def read_item(test_id: int, q: str = None):
    return {"test_id": test_id, "q": q}


# http://127.0.0.1:8000/iris?petal_length=5&petal_width=2&sepal_length=5.3&sepal_width=4
@app.get("/iris")
def iris_classification(petal_length: float,
                        petal_width: float,
                        sepal_length: float,
                        sepal_width: float):
    
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
