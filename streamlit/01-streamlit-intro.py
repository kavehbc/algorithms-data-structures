# first we install streamlit using:
# pip install streamlit

# https://docs.streamlit.io/library/api-reference

import streamlit as st

st.title("Streamlit Intro")

st.write("Hello World!! This is a test.")

title = st.text_input('Movie title', 'Life of Brian')

btn_submit = st.button("Print")

if btn_submit:
    st.write('The current movie title is', title)