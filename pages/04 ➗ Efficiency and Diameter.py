import numpy as np
import pandas as pd
import streamlit as st
from joblib import dump, load

st.set_page_config(layout="centered", page_title="Efficiency and Diameter")

page_css_style = """
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

st.markdown(page_css_style, unsafe_allow_html=True)

# Loads pre-trained models for Efficiency, Diameter and Number of poles

eff_model = load("models/eff_model.joblib")
dia_model = load("models/dia_model.joblib")
poles_model = load("models/poles_model.joblib")


v1, buff, v2 = st.columns([3, 1, 3])

with v1:
    Q = st.number_input(
        "Q:", min_value=1.0, max_value=5000.0, value=10.0, step=1.0, key="Qeff"
    )

with v2:
    H = st.number_input(
        "H:", min_value=1.0, max_value=500.0, value=10.0, step=1.0, key="Heff"
    )

categories = {
    "BB1": "BB - Single-stage",
    "BB2": "BB - Single-stage",
    "BB3": "BB - Multi-stage",
    "BB5": "BB - Multi-stage",
    "OH2": "OH2",
    "OH6": "OH6 - High-speed",
}

poles = {"Two": 2, "Four": 4, "Six": 6}

pred_poles = poles.get(poles_model.predict([[Q, H]])[0])

eff_input = [[1, np.log(Q), np.log(H), np.log(Q) ** 2, np.log(Q) * H, H**2]]
dia_input = [[Q, np.sqrt(H) * pred_poles]]

pred_eff = eff_model.predict(eff_input)
pred_dia = dia_model.predict(dia_input)

v3, buff2, v4 = st.columns([3, 1, 3])

with v1:
    st.metric(label="Efficiency", value=f"{min(90, int(pred_eff))} %")

with v2:
    st.metric(label="Diameter", value=f"{int(pred_dia)} mm")
