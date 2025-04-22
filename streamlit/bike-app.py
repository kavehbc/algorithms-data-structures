import streamlit as st
import requests

def main():
    st.title(':bike: Bike rental prediction')
    
    st.sidebar.subheader('Parameters')
    holiday = int(st.sidebar.toggle('Holiday'))
    working_day = int(st.sidebar.toggle('Working day'))

    weather_options = ['Clear', 'Mist', 'Light rain/snow', 'Heavy rain/snow']
    selected_weather = st.sidebar.selectbox('Weather', weather_options)
    weather = weather_options.index(selected_weather) + 1

    temperature = st.sidebar.slider('Temperature (C)', min_value=0.0, max_value=50.0, step=0.1)
    feels_like = st.sidebar.slider('Feels like (C)', min_value=0.0, max_value=50.0, step=0.1)
    humidity = st.sidebar.slider('Humidity (%)', min_value=0.0, max_value=100.0, step=0.1)
    windspeed = st.sidebar.slider('Windspeed (km/h)', min_value=0.0, max_value=100.0, step=0.1)

    season_options = ['Spring', 'Summer', 'Fall', 'Winter']
    selected_season = st.sidebar.selectbox('Season', season_options)
    season = season_options.index(selected_season) + 1

    date = st.sidebar.date_input("Date", value='today')

    payload = {"holiday": holiday,
        "working_day": working_day,
        "weather": weather,
        "temperature": temperature,
        "feels_like": feels_like,
        "humidity": humidity,
        "windspeed": windspeed,
        "season": season,
        "month": date.month,
        "day": date.day,
        "weekday": date.weekday()}

    req = requests.post("http://localhost:8000/bike", json=payload)
    if req.status_code == 200:
        result = req.json()
        predictions = result["predictions"]
    else:
        predictions = []
    # st.write(predictions)
    st.line_chart(predictions, x_label='Hour')

if __name__ == '__main__':
    main()