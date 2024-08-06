import datetime
import requests

import numpy as np
import pandas as pd
import streamlit as st
import altair as alt

from common import HIDE_ST_STYLE

st.set_page_config(page_title="Risk analysis", page_icon="📈", layout="wide")

st.markdown(HIDE_ST_STYLE, unsafe_allow_html=True)

portfolio1, portfolio2, portfolio3 = st.tabs(["Portfolio1", "Portfolio2", "Prtfolio3"])

with portfolio1:
    gbmparam = requests.get(f"http://127.0.0.1:5000/portfolios/1/gbmparam").json()
    s = gbmparam['s']
    scale = gbmparam['scale']

    gbmplot = requests.get(f"http://127.0.0.1:5000/mathfinance/gbmplot?s={s}&scale={scale}&S0=1)").json()
    axis = gbmplot['axis']
    yearly = gbmplot['yearly']
    df = pd.DataFrame()
    for idx, data in enumerate(yearly):
        temp_df = pd.DataFrame({
            'year': idx + 1,
            'axis': axis,
            'pdf_vals': data['pdf_vals'],
            'exp_90pp': data['exp_90pp']
        })
        df = pd.concat([df, temp_df], ignore_index=True)

    alt_chart = alt.Chart(df).mark_area(
        orient='horizontal',
        opacity=0.5
    ).encode(
        x=alt.X(
            'pdf_vals:Q',
            title=None,
            impute=None,
            axis=alt.Axis(labels=False, values=[0], grid=False, ticks=True)
        ),
        y=alt.Y('axis:Q', title='Value'),
        column=alt.Column('year:N', title='Year from now'),
        tooltip=[
            alt.Tooltip(title="Expected on 90pptile", field='exp_90pp', format=".2f")
        ]
    ).configure_facet(spacing=4).configure_view(stroke=None).properties(width=70)

    st.altair_chart(alt_chart)
