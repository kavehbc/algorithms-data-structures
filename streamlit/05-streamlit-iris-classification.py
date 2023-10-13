import streamlit as st
import pandas as pd
import pickle

def main():
    st.title("Iris Classification")
    sepal_length = st.sidebar.number_input("sepal length (cm)", min_value=4.3, max_value=7.9, step=0.1)
    sepal_width = st.sidebar.number_input("sepal width (cm)", min_value=2.0, max_value=4.4, step=0.1)
    
    petal_length = st.sidebar.number_input("petal length (cm)", min_value=1.0, max_value=6.9, step=0.1)
    petal_width = st.sidebar.number_input("petal width (cm)", min_value=0.1, max_value=2.5, step=0.1)
    
    btn_classify = st.sidebar.button("Classify")
    
    if btn_classify:
        st.write("Button is pressed")
        scaler = pickle.load(open("../objects/iris-scaler.pkl", "rb"))
        model = pickle.load(open("../objects/iris-nn.pkl", "rb"))
        
        columns_to_scale = ['sepal length (cm)', 'sepal width (cm)',
                            'petal length (cm)', 'petal width (cm)']

        df = pd.DataFrame([[sepal_length, sepal_width, petal_length, petal_width]],
                          columns=columns_to_scale)
                          
        st.subheader("Original Dataframe")
        st.write(df)
        
        df[columns_to_scale] = scaler.transform(df[columns_to_scale])

        st.subheader("Scaled Dataframe")
        st.write(df)

        prediction = model.predict(df)
        
        st.subheader("Prediction")
        st.write(prediction)
        
        
if __name__ == "__main__":
    main()
    