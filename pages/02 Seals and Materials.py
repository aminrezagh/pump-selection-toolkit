import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config(layout="centered", page_title="Seal and Material")

hide_streamlit_logo = """
            <style>
            footer {visibility: hidden;}
            #MainMenu {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_logo, unsafe_allow_html=True)

df = pd.read_csv("db/db-v1.5.csv")

liquid = st.text_input("Liquid", key="liquid")

if liquid:
    if df["Liquid"].str.contains(liquid, case=False).any():
        
        # Donut chart for pump seal plan
        fig_seal = px.scatter(df[df["Liquid"].str.contains(liquid, case=False)], 
        x="Project", y="Max. T", size="Qty", color="Seal Plan",
        labels={"Max. T": "Maximum Temperature (°C)"},
        title="Seal Plans",
        color_discrete_sequence=px.colors.qualitative.Pastel)
        fig_seal

        fig_mat = px.scatter(df[df["Liquid"].str.contains(liquid, case=False)], 
        x="Project", y="Min. T", size="Qty", color="Material",
        labels={"Min. T": "Minimum Temperature (°C)"},
        title="Materials",
        color_discrete_sequence=px.colors.qualitative.Pastel)
        fig_mat