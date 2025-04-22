import streamlit as st
import requests


def get_api(url, params):
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None
        
def main():
    st.title("Name Prediction")
    name = st.text_input("Name")
    if len(name) > 0:
        params = {"name": name}
        url = "https://api.genderize.io"
        gender = get_api(url, params)
    
        url = "https://api.nationalize.io"
        nationality = get_api(url, params)
    
        st.write(gender)
        st.write(nationality)
    
if __name__ == "__main__":
    main()
    