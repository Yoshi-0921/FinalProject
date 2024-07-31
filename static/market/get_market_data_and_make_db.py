import pickle
import sqlite3
import time
from datetime import datetime

import pandas as pd

conn = sqlite3.connect('market.sqlite')

# need to execute once on local environment
def save_market_data(symbol):
    dt = datetime(2013, 1, 1)
    start_date = int(round(dt.timestamp()))
    dt = datetime(2023, 1, 1)
    end_date = int(round(dt.timestamp()))
    df = pd.read_csv(f"https://query1.finance.yahoo.com/v7/finance/download/{symbol}?period1={start_date}&period2={end_date}&interval=1d&events=history&includeAdjustedClose=true", parse_dates = ['Date'], index_col='Date')
    df.to_pickle(symbol + ".pkl")

def insert_into_db(symbol):
    df = pd.read_pickle(symbol + ".pkl")
    cur = conn.cursor()
    for date, row in df.iterrows():
        query = "INSERT INTO stocks(unixtimestamp, symbol, open, high, low, close, adjVolume, volume) VALUES ('{}', '{}', {}, {}, {}, {}, {}, {})".format(int(date.timestamp()), str(symbol), row['Open'], row['High'], row['Low'], row['Close'], row['Adj Close'], row['Volume'])
        cur.execute(query)
    conn.commit()

symbols = ["NVDA", "AAPL", "MS"]
for symbol in symbols:
    #save_market_data(symbol)
    insert_into_db(symbol)
conn.close()
