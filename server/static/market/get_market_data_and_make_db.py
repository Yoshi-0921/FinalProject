import pickle
import sqlite3
import time
from datetime import datetime

import pandas as pd

from math import isnan

conn = sqlite3.connect('market.sqlite')

# need to execute once on local environment
def save_market_data(symbol):
    dt = datetime(2010, 4, 1, 9, 0, 0)
    start_date = int(round(dt.timestamp()))
    dt = datetime(2024, 8, 1, 9, 0, 0)
    end_date = int(round(dt.timestamp()))
    df = pd.read_csv(f"https://query1.finance.yahoo.com/v7/finance/download/{symbol}?period1={start_date}&period2={end_date}&interval=1d&events=history&includeAdjustedClose=true", parse_dates = ['Date'], index_col='Date')
    df.to_pickle(symbol + ".pkl")

def insert_into_db(symbol):
    df = pd.read_pickle(symbol + ".pkl")
    cur = conn.cursor()
    for date, row in df.iterrows():
        if isnan(row['Open']) or isnan(row['High']) or isnan(row['Low']) or isnan(row['Close']) or isnan(row['Adj Close']):
            continue
        query = "INSERT INTO stocks(unixtimestamp, symbol, open, high, low, close, adjVolume, volume) VALUES ('{}', '{}', {}, {}, {}, {}, {}, {})".format(int(date.timestamp()), str(symbol), row['Open'], row['High'], row['Low'], row['Close'], row['Adj Close'], 0)
        cur.execute(query)
    conn.commit()

symbols = ["NVDA", "AAPL", "MS", "MSFT", "AMZN", "TSLA", "META", "GOOG", "BRK-B", "XOM", "JNJ", "ARM", "^TNX"]

for symbol in symbols:
    # save_market_data(symbol)
    insert_into_db(symbol)
conn.close()
