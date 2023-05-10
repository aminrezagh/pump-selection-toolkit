import string
import numpy as np
import pandas as pd
import streamlit as st
from joblib import dump, load

st.set_page_config(layout="centered", page_title="API Type")

hide_streamlit_logo = """
            <style>
            footer {visibility: hidden;}
            #MainMenu {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_logo, unsafe_allow_html=True)

# Loads pre-trained models for API-Type and Number of poles
type_model = load("models/type_model.joblib")
poles_model = load("models/poles_model.joblib")


v1, buff, v2 = st.columns([3, 1, 3])

with v1:
    Q = st.number_input('Q:', min_value=1.0, max_value=5000.0, value=10.0, step=1.0, key='Qtype')

with v2:
    H = st.number_input('H:', min_value=1.0, max_value=2500.0, value=10.0, step=1.0, key='Htype')

categories = {"BB1": "BB - Single-stage",
              "BB2": "BB - Single-stage",
              "BB3": "BB - Multi-stage",
              "BB5": "BB - Multi-stage",
              "OH2": "OH2",
              "OH6": "OH6 - High-speed"}

poles = {"Two": 2,
        "Four": 4,
        "Six": 6}

pred_type = categories.get(type_model.predict([[Q, H]])[0])
pred_poles = poles.get(poles_model.predict([[Q, H]])[0])

v3, buff2, v4 = st.columns([3, 1, 3])

with v1:
    st.metric(label="Type", value=pred_type)

with v2:
    st.metric(label="Number of poles", value=pred_poles)