import datetime
import requests

import numpy as np
import pandas as pd
import streamlit as st
import altair as alt
import plotly.graph_objs as go
from scipy import stats

from common import HIDE_ST_STYLE

st.set_page_config(page_title="Risk analysis", page_icon="📈", layout="wide")

st.markdown(HIDE_ST_STYLE, unsafe_allow_html=True)

userid = "weimeng"
portfolio1, portfolio2, portfolio3 = st.tabs(["Portfolio1", "Portfolio2", "Portfolio3"])
portfolios = requests.get(f"http://127.0.0.1:5000/portfolios/{userid}").json()

def render(portfolioid):

    st.header(f"{portfolios['portfolio'][portfolioid - 1][1]}")

    returns = requests.get(f"http://127.0.0.1:5000/returns/{userid}").json()
    symbols = sorted(list(set(status["symbol"] for status in returns[portfolioid - 1]["stocks"])))

    subcol1, subcol2, subcol3 = st.columns([2, 2, 2])
    # Portofolio composition plot
    with subcol1:
        st.subheader("Composition")
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

    gbmparam = requests.get(f"http://127.0.0.1:5000/portfolios/{portfolioid}/gbmparam").json()

    # Variance histogram
    returns = requests.get(f"http://127.0.0.1:5000/portfolios/{portfolioid}/gbmhist").json()
    with subcol2:
        vals = []
        cnts = []
        for bin in returns:
            bucket, low, high, cnt = bin
            vals.append((low + high)/2)
            cnts.append(cnt)

        mean = gbmparam['mean']
        sig = gbmparam['sig']
        normal_dist = stats.norm(mean, sig).pdf(vals)
        normal_dist = normal_dist / np.max(normal_dist) * np.max(cnts)

        df = pd.DataFrame({'val': vals, 'cnt': cnts, 'normal_dist': normal_dist})
        alt_hist = alt.Chart(df).mark_bar().encode(
            x=alt.X('val:Q', title='Variability'),
            y=alt.Y('cnt:Q', title='Occurence')
        )
        alt_norm = alt.Chart(df).mark_line().encode(
            x=alt.X('val:Q', title='Variability'),
            y=alt.Y('normal_dist:Q', title='Occurence'),
            opacity=alt.value(0.6),
            color=alt.value('orange')
        )
        st.subheader("Intraday variance histogram")
        st.altair_chart(alt.layer(alt_hist, alt_norm).properties(height=300, width=400))

    with subcol3:
        mean = gbmparam['mean']
        sig = gbmparam['sig']
        skew = gbmparam['skew']
        kurt = gbmparam['kurt']
        gbmplot = requests.get(f"http://127.0.0.1:5000/mathfinance/gbmEWplot?mean={mean}&sig={sig}").json()
        gbmEWplot = requests.get(f"http://127.0.0.1:5000/mathfinance/gbmEWplot?mean={mean}&sig={sig}&skew={skew}&kurt={kurt}").json()
        df = pd.DataFrame({'val': gbmplot['axis'], 'normal': gbmplot['pdf_vals'], 'ew': gbmEWplot['pdf_vals']})
        alt_chart_normal = alt.Chart(df).mark_area().encode(
            x=alt.X('val:Q', title='Value'),
            y=alt.Y('normal:Q', title='Probability'),
            opacity=alt.value(0.4),
            color=alt.value('orange'),
            tooltip=[
                alt.Tooltip(title="Normal PDF", field='val', format=".4f")
            ]
        )
        alt_chart_EW= alt.Chart(df).mark_area().encode(
            x=alt.X('val:Q', title='Value'),
            y=alt.Y('ew:Q', title='Probability'),
            opacity=alt.value(0.3),
            color=alt.value('green'),
            tooltip=[
                alt.Tooltip(title="Edgeworth 4th PDF", field='val', format=".4f")
            ]
        )
        st.subheader(":orange[Normal] vs. :green[Higher moment aware]")
        st.altair_chart(alt.layer(alt_chart_normal, alt_chart_EW).properties(height=300, width=400))

    st.subheader("20-year forecast")
    # Time evolution plot
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
