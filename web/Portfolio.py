from datetime import datetime

import numpy as np
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import requests
from datetime import datetime
import streamlit as st
import numpy as np
from ta.trend import MACD
from ta.momentum import StochasticOscillator

from common import HIDE_ST_STYLE
from config import NEWS_API_KEY


st.set_page_config(page_title="Portfolio", page_icon="💰", layout="wide")

st.markdown(HIDE_ST_STYLE, unsafe_allow_html=True)

userid = "weimeng"
portfolios = requests.get(f"http://127.0.0.1:5000/portfolios/{userid}").json()

portfolio1, portfolio2 = st.tabs(["Portfolio1", "Portfolio2"])
limit_conversion = {"1W": 7, "1M": 30, "6M": 180, "1Y": 365, "5Y": 1825, "Max": 9999}
company_conversion = {"AAPL": "Apple", "JNJ": "Johnson and Johnson", "NVDA": "Nvidia", "MS": "Morgan Stanley", "MSFT": "Microsoft", "SPY": "S&P 500 Index", "^NDX": "NASDAQ Index"}

def portfolio_page(portfolio_idx):
    import numpy as np
    COL1, COL2 = st.columns([3, 2])
    with COL1:
        returns = requests.get(f"http://127.0.0.1:5000/returns/{userid}").json()
        symbols = sorted(list(set(status["symbol"] for status in returns[portfolio_idx]["stocks"])))

        col1, col2 = st.columns([3, 1])
        with col1:
            st.header(f"{portfolios['portfolio'][portfolio_idx][1]}")
        with col2:
            symbol = st.selectbox(
                "",
                ("Net worth", *symbols),
            )
        if symbol != "Net worth":
            status = returns[portfolio_idx]["stocks"][symbols.index(symbol)]
            b1, b2, b3, b4 = st.columns(4)
            b1.metric(
                "Value",
                "$" + f"{status['value']:.2f}",
                f"{100*status['rateOfReturn']:.2f}" + "%",
            )
            b2.metric("Return", "$" + f"{status['return']:.2f}")
            b3.metric("Share", f"{status['shares']}")
            limit = b4.select_slider(
                "Date range", ["1W", "1M", "6M", "1Y", "5Y", "Max"], "1M", key=f"select_slider_stock_{portfolio_idx}"
            )
        else:
            _value, _return = 0, 0
            for status in returns[portfolio_idx]["stocks"]:
                _value += status["value"]
                _return += status["return"]
            b1, b2, b3 = st.columns(3)
            b1.metric(
                "Value",
                "$" + f"{_value:.2f}",
                f"{100*_return/(_value-_return):.2f}" + "%",
            )
            b2.metric("Return", "$" + f"{_return:.2f}")
            limit = b3.select_slider(
                "Date range", ["1W", "1M", "6M", "1Y", "5Y", "Max"], "1M", key=f"select_slider_{portfolio_idx}"
            )

        if symbol == "Net worth":
            char_data = 0
            for s_idx, s in enumerate(symbols):
                stocks = requests.get(
                    f"http://127.0.0.1:5000/stocks/{s}?limit={limit_conversion[limit]}"
                ).json()
                char_data += returns[portfolio_idx]["stocks"][s_idx][
                    "shares"
                ] * np.asarray([s[6] for s in stocks["stocks"]])
            df = pd.DataFrame(
                {
                    "total": char_data,
                    "timestamp": [
                        datetime.fromtimestamp(s[1]) for s in stocks["stocks"]
                    ],
                }
            )
            st.area_chart(df, x="timestamp", y="total", color="#AAAAFF99", height=250)

            subcol1, subcol2 = st.columns([2, 3])
            with subcol1:
                fig = go.Figure(
                    go.Sunburst(
                        labels=symbols,
                        parents=["stock" for _ in range(len(symbols))],
                        values=[s["value"] for s in returns[portfolio_idx]["stocks"]],
                    )
                )
                fig.update_traces(textinfo="label+percent parent")
                fig.update_layout(margin=dict(t=0, l=0, r=0, b=0), height=230)
                st.plotly_chart(fig, use_container_width=True)

            with subcol2:
                import numpy as np

                df = pd.DataFrame(returns[portfolio_idx]["stocks"])
                df = df.drop(columns=["position_time"])
                st.dataframe(df, key="symbol", hide_index=True, height=230)

        else:
            stocks = requests.get(
                f"http://127.0.0.1:5000/stocks/{symbol}?limit={limit_conversion[limit]}"
            ).json()
            df = pd.DataFrame(
                stocks["stocks"][::-1],
                columns=[
                    "id",
                    "unixtimestamp",
                    "symbol",
                    "open",
                    "high",
                    "low",
                    "close",
                    "adjVolume",
                    "volume",
                    "created_at",
                    "updated_at",
                ],
            )
            df['MA20'] = df['close'].rolling(window=20).mean() # .shift(-19)
            df['MA5'] = df['close'].rolling(window=5).mean() # .shift(-4)
            timestamps = [ts for ts in df["unixtimestamp"]]
            try:
                timestamp = timestamps.index(status["position_time"])
            except ValueError:
                timestamp = 0 # len(df)
            bdf = df[:timestamp]
            hdf = df[timestamp:]

            macd = MACD(close=df['close'],
                    window_slow=26,
                    window_fast=12,
                    window_sign=9)
            stoch = StochasticOscillator(high=df['high'],
                                        close=df['close'],
                                        low=df['low'],
                                        window=14,
                                        smooth_window=3)

            fig = make_subplots(rows=4, cols=1, shared_xaxes=True, row_heights=[0.40,0.2,0.2,0.20])
            fig.add_trace(
                go.Candlestick(
                        x=[datetime.fromtimestamp(ts) for ts in bdf["unixtimestamp"]],
                        open=bdf["open"],
                        high=bdf["high"],
                        low=bdf["low"],
                        close=bdf["close"],
                        name="Backtest",
                        increasing=dict(fillcolor="#99703D", line=dict(color="#99703D")),
                        decreasing=dict(fillcolor="#4136FF", line=dict(color="#4136FF"))
                    ), row=1, col=1)
            fig.add_trace(
                go.Candlestick(
                        x=[datetime.fromtimestamp(ts) for ts in hdf["unixtimestamp"]],
                        open=hdf["open"],
                        high=hdf["high"],
                        low=hdf["low"],
                        close=hdf["close"],
                        name="Holding",
                        increasing=dict(fillcolor="#3D9970", line=dict(color="#3D9970")),
                        decreasing=dict(fillcolor="#FF4136", line=dict(color="#FF4136"))
                    ), row=1, col=1
            )
            fig.add_trace(
                go.Scatter(
                        x=[datetime.fromtimestamp(ts) for ts in timestamps],
                        y=df['MA5'],
                        opacity=0.7,
                        line=dict(color='blue', width=2),
                        name='MA 5'
                    ), row=1, col=1
            )
            fig.add_trace(
                go.Scatter(
                        x=[datetime.fromtimestamp(ts) for ts in timestamps],
                        y=df['MA20'],
                        opacity=0.7,
                        line=dict(color='orange', width=2),
                        name='MA 20'
                    ), row=1, col=1
            )
            if timestamp != 0:
                fig.add_hline(y=df['close'][timestamp], line=dict(color='tomato', width=2), row=1, col=1)


            fig.add_trace(go.Bar(x=[datetime.fromtimestamp(ts) for ts in timestamps],
                                y=df['volume']
                                ), row=2, col=1)
            # Plot MACD trace on 3rd row
            fig.add_trace(go.Bar(x=[datetime.fromtimestamp(ts) for ts in timestamps],
                                y=macd.macd_diff()
                                ), row=3, col=1)
            fig.add_trace(go.Scatter(x=[datetime.fromtimestamp(ts) for ts in timestamps],
                                    y=macd.macd(),
                                    line=dict(color='black', width=2)
                                    ), row=3, col=1)
            fig.add_trace(go.Scatter(x=[datetime.fromtimestamp(ts) for ts in timestamps],
                                    y=macd.macd_signal(),
                                    line=dict(color='blue', width=1)
                                    ), row=3, col=1)
            # Plot stochastics trace on 4th row
            fig.add_trace(go.Scatter(x=[datetime.fromtimestamp(ts) for ts in timestamps],
                                    y=stoch.stoch(),
                                    line=dict(color='black', width=2)
                                    ), row=4, col=1)
            fig.add_trace(go.Scatter(x=[datetime.fromtimestamp(ts) for ts in timestamps],
                                    y=stoch.stoch_signal(),
                                    line=dict(color='blue', width=1)
                                    ), row=4, col=1)

            fig.update_layout(
                xaxis_rangeslider_visible=False,showlegend=False,
                margin={"t": 0, "l": 0, "b": 0, "r": 0}, height=500
            )
            st.plotly_chart(fig, use_container_width=True)

    with COL2:
        feed = 4
        if symbol == "Net worth":
            query = "Market today"
        else:
            query = f"{company_conversion[symbol]} Market"
        news = requests.get(
            f"https://newsapi.org/v2/everything?q={query}&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
        ).json()
        for i in range(feed):
            story = news["articles"][i]
            title = story["title"]
            url = story["url"]
            urlToImage = story["urlToImage"]
            publishedAt = story["publishedAt"]

            if title is not None and urlToImage is not None and publishedAt is not None:
                col1, col2 = st.columns([1, 3])
                with col1:
                    if urlToImage is not None:
                        st.image(urlToImage, width=100)
                with col2:
                    st.markdown(f"[{title}]({url})")
                    st.text(publishedAt)
                st.markdown("""---""")

with portfolio1:
    portfolio_page(0)

with portfolio2:
    portfolio_page(1)
