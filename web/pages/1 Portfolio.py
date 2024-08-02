import pandas as pd
import plotly.graph_objs as go
import requests
import streamlit as st
from common import HIDE_ST_STYLE
from plotly.subplots import make_subplots
import numpy as np
from web.config import NEWS_API_KEY

st.set_page_config(page_icon=':star', layout='wide')

st.markdown(HIDE_ST_STYLE, unsafe_allow_html=True)

userid = "weimeng"
portfolios = requests.get(f"http://127.0.0.1:5000/portfolios/{userid}").json()

portfolio1, portfolio2, portfolio3 = st.tabs(["Portfolio1", "Portfolio2", "Prtfolio3"])

with portfolio1:
    COL1, COL2 = st.columns([3,2])
    with COL1:
        returns = requests.get(f"http://127.0.0.1:5000/returns/{userid}").json()
        symbols = list(set(status["symbol"] for status in returns[0]["stocks"]))

        col1, col2 = st.columns([3,1])
        with col1:
            st.header(f"{portfolios['portfolio'][0][1]}")
        with col2:
            symbol = st.selectbox(
                "",
                ("Net worth", *symbols),
            )
        if symbol!="Net worth":
            status = returns[0]["stocks"][symbols.index(symbol)]
            b1, b2, b3, b4 = st.columns(4)
            b1.metric("Value", "$"+f"{status['value']:.2f}", f"{100*status['rateOfReturn']:.2f}"+"%")
            b2.metric("Return", "$"+f"{status['return']:.2f}")
            b3.metric("Share", f"{status['shares']}")
            limit = b4.select_slider("Date range", [7, 50, 100, 500, 1000, 2000, 3000, "max"],100)
        else:
            _value, _return = 0, 0
            for status in returns[0]["stocks"]:
                _value += status['value']
                _return += status['return']
            b1, b2, b4 = st.columns(3)
            b1.metric("Value", "$"+f"{_value:.2f}", f"{100*_return/(_value-_return):.2f}"+"%")
            b2.metric("Return", "$"+f"{_return:.2f}")
            limit = b4.select_slider("Date range", [7, 50, 100, 500, 1000, 2000, 3000, "max"],100)

        if symbol == "Net worth":
            char_data = 0
            for s in symbols:
                stocks = requests.get(f"http://127.0.0.1:5000/stocks/{s}?limit={limit}").json()
                char_data += returns[0]["stocks"][symbols.index(s)]["shares"] * np.asarray([s[6] for s in stocks["stocks"]])
            st.area_chart(char_data[::-1], color="#AAAAFF99", height=250)

            subcol1, subcol2 = st.columns([2,3])
            with subcol1:
                fig =go.Figure(go.Sunburst(
                    labels=symbols,
                    parents=['stock' for _ in range(len(symbols))],
                    values=[status['value'] for status in returns[0]["stocks"]],
                ))
                fig.update_traces(textinfo="label+percent parent")
                fig.update_layout(margin = dict(t=0, l=0, r=0, b=0), height=230)
                st.plotly_chart(fig, use_container_width=True)

            with subcol2:
                import numpy as np
                df = pd.DataFrame(
                    np.random.randn(10, 5), columns=("col %d" % i for i in range(5))
                )
                st.dataframe(df, height=230)

        else:
            stocks = requests.get(f"http://127.0.0.1:5000/stocks/{symbol}?limit={limit}").json()
            df = pd.DataFrame(stocks["stocks"], columns=['id', 'unixtimestamp', 'symbol', 'open', 'high', 'low', 'close', 'adjVolume', 'volume', 'created_at', 'updated_at'])
            timestamps = [ts for ts in df['unixtimestamp']]
            try:
                timestamp = timestamps.index(status['position_time'])
            except ValueError:
                timestamp = len(df)
            bdf = df[timestamp:]
            hdf = df[:timestamp]

            fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                vertical_spacing=0.03, subplot_titles=('OHLC', 'Volume'),
                row_width=[0.2, 0.7])

            candlestick_chart = go.Figure(data=[go.Candlestick(x=bdf['unixtimestamp'],open=bdf['open'], high=bdf['high'], low=bdf['low'], close=bdf['close'], name="Backtest")])
            candlestick_chart.update_layout(xaxis_rangeslider_visible=False)
            # candlestick_chart.update_layout(title=f"{symbol} Candlestick Chart", xaxis_rangeslider_visible=False)
            candlestick_chart.add_traces(go.Candlestick(x=hdf['unixtimestamp'],open=hdf['open'], high=hdf['high'], low=hdf['low'], close=hdf['close'], name="Holding"))
            candlestick_chart.add_hline(y=df['close'][timestamp-1], line_width=2, line_color="tomato")

            candlestick_chart.data[0].increasing.fillcolor = '#99703D'
            candlestick_chart.data[0].increasing.line.color ='#99703D'
            candlestick_chart.data[0].decreasing.fillcolor = '#4136FF'
            candlestick_chart.data[0].decreasing.line.color = '#4136FF'
            candlestick_chart.data[1].increasing.fillcolor = '#3D9970'
            candlestick_chart.data[1].increasing.line.color = '#3D9970'
            candlestick_chart.data[1].decreasing.fillcolor = '#FF4136'
            candlestick_chart.data[1].decreasing.line.color = '#FF4136'
            candlestick_chart.update_layout(margin={'t':0,'l':0,'b':0,'r':0}, height=250)
            st.plotly_chart(candlestick_chart, use_container_width=True)

    with COL2:
        feed = 4
        if symbol == "Net worth":
            query = "Market today"
        else:
            query = f"{symbol} Market"
        news = requests.get(f"https://newsapi.org/v2/everything?q={query}&sortBy=publishedAt&apiKey={NEWS_API_KEY}").json()
        for i in range(feed):
            story = news["articles"][i]
            title = story["title"]
            url = story["url"]
            urlToImage = story["urlToImage"]
            publishedAt = story["publishedAt"]
            # publishedAt = format_date(story["publishedAt"])

            if title is not None and urlToImage is not None and publishedAt is not None:
                col1, col2 = st.columns([1, 3])
                with col1:
                    if urlToImage is not None:
                        st.image(urlToImage, width=100)
                with col2:
                    st.markdown(f'[{title}]({url})')
                    st.text(publishedAt)
                st.markdown("""---""")

with portfolio2:
    col1, col2 = st.columns([3,1])
    with col1:
        st.header("Portfolio 2")
    # with col2:
        # symbol = st.selectbox(
        #     "",
        #     ("Net worth", ),
        # )
    stocks = requests.get(f"http://127.0.0.1:5000/stocks/GOOG").json()
    char_data = pd.DataFrame([s[6] for s in stocks["stocks"]])
    st.line_chart(char_data)

with portfolio3:
    col1, col2 = st.columns([3,1])
    with col1:
        st.header("Portfolio 3")
    # with col2:
    #     symbol = st.selectbox(
    #         "",
    #         ("Net worth", ),
    #     )
    stocks = requests.get(f"http://127.0.0.1:5000/stocks/MSFT").json()
    char_data = pd.DataFrame([s[6] for s in stocks["stocks"]])
    st.line_chart(char_data)
