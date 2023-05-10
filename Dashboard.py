import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config(layout="centered", page_title="Dashboard")

hide_streamlit_logo = """
            <style>
            footer {visibility: hidden;}
            #MainMenu {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_logo, unsafe_allow_html=True)

df = pd.read_csv("db/db-v1.5.csv")

proj = st.multiselect("Project", set(df["Project"]), key="proj_sel")

if proj:
    # Donut chart for pump type
    fig_type = px.pie(df[df["Project"].isin(proj)], values="Qty", names="Type", title='Type',
                      color_discrete_sequence=px.colors.qualitative.Pastel)
    fig_type.update_traces(hole=0.4)
    fig_type

    # Donut chart for pump seal plan
    fig_seal = px.pie(df[df["Project"].isin(proj)], values="Qty", names="Seal Plan", title='Seal Plan',
                      color_discrete_sequence=px.colors.qualitative.Pastel)
    fig_seal.update_traces(hole=0.4)
    fig_seal

    # Donut chart for pump material
    fig_mat = px.pie(df[df["Project"].isin(proj)], values="Qty", names="Material", title='Material',
                     color_discrete_sequence=px.colors.qualitative.Pastel)
    fig_mat.update_traces(hole=0.4)
    fig_mat
else:
    fig_proj = px.bar(df.groupby("Project").sum().reset_index(), x="Project", y="Qty",
                      labels={"Qty": "Quantity"},
                      color_discrete_sequence=px.colors.qualitative.Pastel)
    fig_proj