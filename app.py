import streamlit as st
import numpy as np
import pandas as pd

file = st.file_uploader(label="select file ")

df = pd.read_csv(file, delimiter="\s+")


def predict():
    st.success(f"{df.columns}")


st.button("Predict", on_click=predict)
