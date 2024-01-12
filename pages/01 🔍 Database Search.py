import numpy as np
import pandas as pd
import streamlit as st
import socket

CSV_FILE_PATH = "db/db-v1.5.csv"
PAGE_STYLE = """
            <style>
            footer {visibility: hidden;}
            #MainMenu {visibility: hidden;}
            .stDeployButton {visibility: hidden;}
            .main {
                background-image: url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAAAXNSR0IArs4c6QAABKpJREFUeF7tnduygyAMRWv7/5/c9gzO0GFy0FyBRNPXKsa92IQgttv3+/0+8uNGgS2BuGGxB5JAfPFIIM54JJAE4k0BZ/FkDkkgzhRwFk46JIE4U8BZOJdwSFls2LbNmbSycMIDKTDq6s/z+ZSp4Ois0EAKiM/n85OzuCQ6lLBAqjPg2mh0KCGBQGfAEScylHBAjpxxFSihgGDOuAKUMECozogOJQQQrjMiQ3EPROqMqFDcAynCah1S4USYfYUAUgQtBaDFfgzvUFwCqcLD9ak7OMUdkHZtqgCBUK7uFFdAeg4oa1N3coobIGdrU3dyigsglNxwF6csB0KtM6pLrp5TlgKhOAMWeFd3yjIgVGf0Ku4r55QlQCTOuItTpgOROoO6NhW9TpkKxMIZ+5Z95Nn5rOuM2BsxDUjdjKBdj8JgVJGiOmUKkJHi1CGwt9skolOGAxnpjFbwq9QpQ4GMdMZR29HrlGFARs6mMNC9PIOdQ03Q1BxGbe/f7HHES58jb57adk+4CDnF3CErnUGpVahAsR4+yimmQEberLTtaE4xAzJrNoX13N73vUQvBUxxoSTG30YMixwy+ua07R8NLx5zitohI51huQXo9Xp1O64WtvUWIxWQGTdj1YuPgFhCt0j0YiAzYFiKdQbE074vEZBZMGYCsbyWxilsICPrjN4gP2PIaq9r1dl6MzvK7IsNxCJgbg/SXpN7PYtOcLTYiUFhAbEKlPti5mwgVjmF2xH2h2+cOmSFMNoHThJR6jUtOiA2mRAvLmpzh0YYTcKVjuXajlDP516f7BANEC0MSdKVjuHWEwvuvbOAtC/pY8nJuoJth5F2h3wvDq4IlHuRDtfcWMhApAFxLUsRpz2mwultnuO2hR0v0cAdkBlCYUJafI+58ugaw4BYzDgshInWRgJxRmwoEKltnWk0NRxuDiUndavqdaoaDi42rDDUFGcOdFkSAne4Yi+dpEvoXKWFKWvIqi7JXIKDkbhD5JB0yTgYYiAJ5RiK1Bm1RfaQBZctJOtbeB+LeYQWhsohVTLNKnBM2f9HLU3gvftXOQS65W7JvoDYe3XnN1mknc0MCIRTZ2TSwLye10IYEeMQICMCvUubCcQZ6QSSQJwp4CycaQ7hzMDafVvwPLini1oHwZkQFo/lzInDfBoQ6vNoWFzBV58hkPf7Tbpf+FyCGg/3eQYpmJODEgiioGXRR4G1BAhniYHqEK5wrUOwV9448VJEPzsmgTwe+5/A1IKvXRJq8xP3yZ8UzDIgUIB6A2fC9HpqzSFYEobtYg4p8VCOkQp/dN4SIGc3AXsrdcg6HQY6P+dEEZtyTAIBf/xFmWX1nEURm3LMJYCcDS+aIauuvPZEyiELqNL2Ns6shTpkWc+y4HOeyyd16ltUq4BIO5B2CFuS1DkzIi4QLLnX76Hg7ZAGl1U4jg4JBBOtBUYFggkBRYVLJxBIOw2nuhmLgfL9Eod4BAJjqoBmwtgnJZyXPimEj44pPZ366c20zgpHSbuUeI6KV+r1JMdNAyIJ7o7nJBBn1BNIAnGmgLNw0iEJxJkCzsJJhyQQZwo4CycdkkCcKeAsnHRIAnGmgLNw/gAOvtkgXy6PIAAAAABJRU5ErkJggg==');
                background-size: 100px;
            }
            </style>
            """


def generate_scope(conditions):
    result = []

    for var, expr in conditions.items():
        if eval(var):
            result.append(expr)

    return " & ".join(result)


def get_network_ip():
    try:
        host_ip = socket.gethostbyname("host.docker.internal")
    except socket.gaierror:
        host_ip = None
    return host_ip


st.set_page_config(page_icon="🔍", layout="wide", page_title="Database Search")
st.markdown(PAGE_STYLE, unsafe_allow_html=True)

# Get the local network IP address
if "network_ip" not in st.session_state:
    st.session_state["network_ip"] = get_network_ip()

df = pd.read_csv(CSV_FILE_PATH)
df["GA"] = f"http://{st.session_state['network_ip']}:8000/" + df["GA"].str.replace(
    "\\", "/"
)

COL_CONFIG = {"GA": st.column_config.LinkColumn(display_text="Open GAD")}

searchable_cols = [
    "Service",
    "Liquid",
    "Q",
    "H",
    "Type",
    "Min. T",
    "T",
    "Max. T",
    "Pv",
    "Density",
    "Viscosity",
    "Min. Ps",
    "Max. Ps",
    "Pd",
    "NPSHR",
    "Power",
    "Rated dia.",
    "Forced Lubrication",
    "Seal Plan",
    "Material",
    "Project",
    "Vendor",
]


string_cols = ["Service", "Liquid"]

cols = st.multiselect("Data Columns", df[searchable_cols].columns.to_list())

search_dict = {}
# initializes options list for categorical data
opts = []
# initializes range list for numerical data
rngs = []

if cols:
    for col, val in df[cols].items():
        if col in string_cols:
            search_dict[col] = st.text_input(col, key=col)

        # checks whether selected data-type is categorical
        elif df[col].dtype == "O":
            opts += st.multiselect(col, sorted(set(val) - {np.nan}), key=col)

        else:
            # stores the minimum and maximum value of a numerical column
            col_min, col_max = df[col].min(), df[col].max()
            st.caption(f"{col}")

            # creates vertical columns for styling
            v1, buff, v2 = st.columns([2, 3, 2])

            with v1:
                first_input = st.number_input(
                    "From:",
                    min_value=col_min,
                    max_value=col_max,
                    value=col_min,
                    key=f"{col} 1",
                )

            with v2:
                second_input = st.number_input(
                    "To:",
                    min_value=col_min,
                    max_value=col_max,
                    value=col_max,
                    key=f"{col} 2",
                )

            start_val, end_val = min(first_input, second_input), max(
                first_input, second_input
            )

            # adds detected range to the range list (column name included)
            rngs += [(col, start_val, end_val)]

    # checks whether column values lie within the selected range and returns a boolean
    bool_list = [((df[c] >= l) & (df[c] <= h)) for c, l, h in rngs]

    # defines two intermediate variables for column selection
    diff_cols = list(set(cols).difference(set(string_cols)))

    CONDITIONS = {
        "rngs": "pd.DataFrame(bool_list).T.all(axis=1)",
        "search_dict": "pd.DataFrame([df[c].str.contains(v, case=False) for c, v in search_dict.items()]).T.all(axis=1)",
        "True": "df[diff_cols].select_dtypes(include=['object']).isin(opts).all(axis=1)",
    }

    st.dataframe(
        df[
            # filters data based on combined conditions
            eval(generate_scope(CONDITIONS))
        ],
        column_config=COL_CONFIG,
        hide_index=True,
    )
