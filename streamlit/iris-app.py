import streamlit as st
import requests
import base64


def main():
    st.title("IRIS Classification")

    petal_length = st.number_input("Petal Length", value=1.4, min_value=1.0, max_value=6.9, step=0.1)
    petal_width = st.number_input("Petal Width", value=0.2, min_value=0.1, max_value=2.5, step=0.1)
    sepal_length = st.number_input("Sepal Length", value=4.9, min_value=4.3, max_value=7.9, step=0.1)
    sepal_width = st.number_input("Sepal Width", value=3.0, min_value=2.0, max_value=4.4, step=0.1)
    classify = st.button("Classify")

    if classify:
        url = f"http://127.0.0.1:8000/iris?"
        url += f"petal_length={petal_length}&petal_width={petal_width}"
        url += f"&sepal_length={sepal_length}&sepal_width={sepal_width}"

        st.write(url)
        
        response = requests.get(url)
        if response.status_code == 200:
            result = response.json()

            class_name = result["class"]
            img = result["image"]
            img_decoded = base64.b64decode(img)
            
            st.info(class_name)
            st.image(img_decoded)
        else:
            st.error(response.json())        


if __name__ == "__main__":
    main()
    