import streamlit as st
import numpy as np
import pandas as pd

file = st.file_uploader(label="select file ")

def predict():
    
    df = pd.read_csv(file, delimiter="\s+")
    st.success(f"{df.columns}")


st.button("Predict", on_click=predict)
