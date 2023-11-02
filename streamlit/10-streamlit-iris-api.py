import streamlit as st
import requests


def main():
    st.title("Iris API")
    sepal_length = st.sidebar.number_input("sepal length (cm)", min_value=4.3, max_value=7.9, step=0.1)
    sepal_width = st.sidebar.number_input("sepal width (cm)", min_value=2.0, max_value=4.4, step=0.1)
    
    petal_length = st.sidebar.number_input("petal length (cm)", min_value=1.0, max_value=6.9, step=0.1)
    petal_width = st.sidebar.number_input("petal width (cm)", min_value=0.1, max_value=2.5, step=0.1)
    
    btn_classify = st.sidebar.button("Classify")
    
    if btn_classify:
        st.write("Button is pressed")
        
        url = f"http://127.0.0.1:8000/iris?petal_length={petal_length}&petal_width={petal_width}&sepal_length={sepal_length}&sepal_width={sepal_width}"
        
        api = requests.get(url)
        result = api.json()
        
        st.write(result)

        st.subheader(f"Classification: {result['prediction']['name']}")
    
    
if __name__ == "__main__":
    main()
    