import streamlit as st
import requests
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from common import HIDE_ST_STYLE
st.set_page_config(page_icon=':star', layout='wide')

st.markdown(HIDE_ST_STYLE, unsafe_allow_html=True)

userid = "weimeng"
portfolios = requests.get(f"http://127.0.0.1:5000/portfolios/{userid}").json()

portfolio1, portfolio2, portfolio3 = st.tabs(["Portfolio1", "Portfolio2", "Prtfolio3"])

with portfolio1:
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
        b1, b2, _, _ = st.columns(4)
        b1.metric("Value", "$"+f"{_value:.2f}", f"{100*_return/(_value-_return):.2f}"+"%")
        b2.metric("Return", "$"+f"{_return:.2f}")

    if symbol == "Net worth":
        stocks = requests.get(f"http://127.0.0.1:5000/stocks/GOOG?limit=250").json()
        char_data = pd.DataFrame([s[6] for s in stocks["stocks"]])
        st.line_chart(char_data, color=(0,0,255))

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

        candlestick_chart.data[0].increasing.fillcolor = '#99703D'
        candlestick_chart.data[0].increasing.line.color ='#99703D'
        candlestick_chart.data[0].decreasing.fillcolor = '#4136FF'
        candlestick_chart.data[0].decreasing.line.color = '#4136FF'
        candlestick_chart.data[1].increasing.fillcolor = '#3D9970'
        candlestick_chart.data[1].increasing.line.color = '#3D9970'
        candlestick_chart.data[1].decreasing.fillcolor = '#FF4136'
        candlestick_chart.data[1].decreasing.line.color = '#FF4136'
        candlestick_chart.update_layout(margin={'t':0,'l':0,'b':0,'r':0}, height=300)

        st.plotly_chart(candlestick_chart, use_container_width=True)

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
