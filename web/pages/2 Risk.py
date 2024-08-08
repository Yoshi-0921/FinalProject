import datetime
import requests

import numpy as np
import pandas as pd
import streamlit as st
import altair as alt
import plotly.graph_objs as go

from common import HIDE_ST_STYLE

st.set_page_config(page_title="Risk analysis", page_icon="📈", layout="wide")

st.markdown(HIDE_ST_STYLE, unsafe_allow_html=True)

userid = "weimeng"
portfolio1, portfolio2, portfolio3 = st.tabs(["Portfolio1", "Portfolio2", "Portfolio3"])
portfolios = requests.get(f"http://127.0.0.1:5000/portfolios/{userid}").json()

def render(portfolioid):

    st.header(f"{portfolios['portfolio'][portfolioid - 1][1]}")

    # Portofolio timeseries stat
    returns = requests.get(f"http://127.0.0.1:5000/returns/{userid}").json()
    symbols = sorted(list(set(status["symbol"] for status in returns[portfolioid - 1]["stocks"])))

    subcol1, subcol2 = st.columns([2, 3])
    with subcol1:
        fig = go.Figure(
            go.Sunburst(
                labels=symbols,
                parents=["stock" for _ in range(len(symbols))],
                values=[s["value"] for s in returns[portfolioid - 1]["stocks"]],
            )
        )
        fig.update_traces(textinfo="label+percent parent")
        fig.update_layout(margin=dict(t=0, l=0, r=0, b=0), height=230)
        st.plotly_chart(fig, use_container_width=True)

    returns = requests.get(f"http://127.0.0.1:5000/portfolios/{portfolioid}/gbmhist").json()
    with subcol2:
        vals = []
        cnts = []
        for bin in returns:
            bucket, low, high, cnt = bin
            vals.append((low + high)/2)
            cnts.append(cnt)
        df = pd.DataFrame({'val': vals, 'cnt': cnts})
        alt_chart = alt.Chart(df).mark_bar().encode(
            x=alt.X('val:Q', title='Variability'),
            y=alt.Y('cnt:Q', title='Occurence')
        )
        st.altair_chart(alt_chart)


    # Time evolution plot
    gbmparam = requests.get(f"http://127.0.0.1:5000/portfolios/{portfolioid}/gbmparam").json()
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
            'q25': data['q25'],
            'q75': data['q75'],
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
            alt.Tooltip(title="Expected value on 90pctile", field='exp_90pp', format=".2f"),
            alt.Tooltip(title="25pctile", field='q25', format=".2f"),
            alt.Tooltip(title="75pctile", field='q75', format=".2f")
        ]
    ).configure_facet(spacing=3).configure_view(stroke=None).properties(width=50)

    st.altair_chart(alt_chart)

with portfolio1:
    render(1)

with portfolio2:
    render(2)

with portfolio3:
    render(3)
