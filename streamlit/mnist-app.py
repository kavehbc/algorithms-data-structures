import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import io
import requests

def classify(data):
    api_url = "http://localhost:8000/image/"
    files = {"image": data}

    res = requests.post(api_url, files=files)
    if res.status_code == 200:
        result = res.json()
        prediction = result["class"]
        return prediction
    return None
    
def main():
    st.title("MNIST Classifier")
    tab_canvas, tab_files = st.tabs(["Canvas", "Upload File"])
    
    with tab_canvas:
        canvas_result = st_canvas(fill_color = "rgba(255, 165, 0, 1)",
                                  stroke_width = 50,
                                  stroke_color = "#FFFFFF",
                                  background_color = "#000000",
                                  background_image = None,
                                  update_streamlit=True,
                                  height = 400,
                                  width = 400,
                                  drawing_mode="freedraw",
                                  point_display_radius= 0,
                                  display_toolbar=True,
                                  key="full_app")
        if canvas_result.image_data is not None:
            data = canvas_result.image_data
            img = Image.fromarray(data).resize((28, 28))
            st.image(img)

            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()

            prediction = classify(img_byte_arr)
            st.subheader(prediction)

    
    with tab_files:
        uploaded_files = st.file_uploader("Upload your image",
                                          accept_multiple_files=True,
                                          type=["jpg", "png"])
        if uploaded_files is not None:
            for file in uploaded_files:
                data = file.getvalue()
                st.image(data)
                prediction = classify(data)
                st.subheader(prediction)

        
        
if __name__ == "__main__":
    main()