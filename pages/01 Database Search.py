import numpy as np
import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode

st.set_page_config(layout="wide", page_title="Search")

hide_streamlit_logo = """
            <style>
            footer {visibility: hidden;}
            #MainMenu {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_logo, unsafe_allow_html=True)
    
df = pd.read_csv("db/db-v1.5.csv")

# Sets tha AgGrid parameters
gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_selection(selection_mode="multiple")
gb.configure_default_column(filterable=False, editable=False)
gb.configure_column("GA", cellRenderer=JsCode(""" function(params) {
                                                        if (params.value != "nan"){
                                                            return `<a href="http://w2859.main.com:8000/${params.value}" 
                                                            target="_blank">Open GAD</a>`}
                                                        }
                                                """))
gbo = gb.build()

searchable_cols = ['Service', 'Liquid', 'Q', 'H', 'Type', 'Min. T', 'T', 'Max. T',
         'Pv', 'Density', 'Viscosity', 'Min. Ps', 'Max. Ps', 'Pd', 'NPSHR', 
         'Power', 'Rated dia.', 'Forced Lubrication', 'Seal Plan', 
         'Material', 'Project', 'Vendor']


string_cols = ['Service', 'Liquid']

cols = st.multiselect("Data Columns", df[searchable_cols].columns.to_list())

search_str = []
# initializes options list for categorical data
opts = []
# initializes range list for numerical data
rngs = []

if cols:
    for col, val in df[cols].iteritems():

        if col in string_cols:
            search_str += [st.text_input(col, key=col)]

        # checks whether selected data-type is categorical
        elif df[col].dtype == "O":
            opts += st.multiselect(col, sorted(set(val) - {np.nan}), key=col)
        
        else:
            # stores the minimum and maximum value of a numerical column
            col_min, col_max = df[col].min(), df[col].max()
            st.caption(f'{col}')
            
            # creates vertical columns for styling 
            v1, buff, v2 = st.columns([2, 3, 2])
            
            with v1:
                first_input = st.number_input('From:', min_value=col_min, max_value=col_max, value=col_min,
                key=f'{col} 1')

            with v2:
                second_input = st.number_input('To:', min_value=col_min, max_value=col_max, value=col_max,
                key=f'{col} 2')

            start_val, end_val = min(first_input, second_input), max(first_input, second_input)

            # adds detected range to the range list (column name included)
            rngs += [(col, start_val, end_val)]

    # checks whether column values lie within the selected range and returns a boolean
    bool_list = [((df[c] >= l) & (df[c] <= h)) for c, l, h in rngs]

    # defines two intermediate variables for column selection 
    diff_cols = list(set(cols).difference(set(string_cols)))
    inter_cols = list(set(cols).intersection(set(string_cols)))

    if rngs:
        AgGrid(df[
                # filters data based on combined conditions
                df[diff_cols].select_dtypes(include=["object"]).isin(opts).all(axis=1)
                & pd.DataFrame(bool_list).T.all(axis=1)
                & df[inter_cols].apply(lambda r: r.str.contains('|'.join(search_str), case=False)).all(axis=1)
            ], height=450, theme="streamlit", gridOptions=gbo, allow_unsafe_jscode=True)

    elif opts or search_str:
        AgGrid(df[
                # filters data based on combined conditions
                df[diff_cols].select_dtypes(include=["object"]).isin(opts).all(axis=1)
                & df[inter_cols].apply(lambda r: r.str.contains('|'.join(search_str), case=False)).all(axis=1)
            ], height=450, theme="streamlit", gridOptions=gbo, allow_unsafe_jscode=True)
