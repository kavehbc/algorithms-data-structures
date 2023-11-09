import streamlit as st
import requests


def main():
    st.write("MNIST CNN Classifier")

    uploaded_file = st.file_uploader("Choose a file")
    
    btn_classify = st.button("Classify")
    
    if btn_classify and uploaded_file is not None:
        st.write("Button is pressed")
        
        image_binary = uploaded_file.read()
        
        image = {'file': image_binary}
        url = f"http://127.0.0.1:8000/mnist"
        
        api = requests.post(url, files=image)
        result = api.json()
        
        st.write(result)

        st.subheader(f"Classification: {result['prediction']}")
    
    
if __name__ == "__main__":
    main()
    