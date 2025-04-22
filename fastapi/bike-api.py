from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import pickle
import pandas as pd
import numpy as np

app = FastAPI(title="Bike Sharing")

def sin_cos(value, length):
    sin_value = np.sin(2 * np.pi * value / length)
    cos_value = np.cos(2 * np.pi * value / length)
    return sin_value, cos_value
    
@app.get("/")
def homepage():
    return {"hello": "world"}

class Bike(BaseModel):
    holiday: bool
    working_day: bool
    weather: int
    temperature: float
    feels_like: float
    humidity: float
    windspeed: float
    season: int
    month: int
    day: int
    weekday: int
    
@app.post("/bike")
def bike(payload: Bike):
    season_sin, season_cos = sin_cos(payload.season, 4) 
    month_sin, month_cos = sin_cos(payload.month, 12)
    day_sin, day_cos = sin_cos(payload.day, 19)
    weekday_sin, weekday_cos = sin_cos(payload.weekday, 7)
    
    scaler = pickle.load(open('bike-scaler.pkl', 'rb'))
    model = pickle.load(open('bike-model.pkl', 'rb'))

    columns = ['holiday', 'workingday', 'weather', 'temp', 'atemp', 'humidity',
       'windspeed', 'season_sin', 'season_cos', 'month_sin', 'month_cos',
       'day_sin', 'day_cos', 'weekday_sin', 'weekday_cos', 'hour_sin',
       'hour_cos']

    data = []
    
    for hour in range(24):
        hour_sin, hour_cos = sin_cos(hour, 24)
        data.append([payload.holiday, payload.working_day, payload.weather,
                     payload.temperature, payload.feels_like,
                     payload.humidity, payload.windspeed, season_sin, season_cos, month_sin, month_cos,
                     day_sin, day_cos, weekday_sin, weekday_cos, hour_sin, hour_cos])

    df = pd.DataFrame(data=data, columns=columns)

    features_to_scale = ['weather', 'temp', 'atemp', 'humidity', 'windspeed']
    df[features_to_scale] = scaler.transform(df[features_to_scale])

    predictions = model.predict(df)
    predictions = np.expm1(predictions)

    return {"predictions": predictions.tolist()}
    
if __name__ == "__main__":
    uvicorn.run(app="bike-api:app",
                port=8000,
                host="0.0.0.0",
                reload=True)