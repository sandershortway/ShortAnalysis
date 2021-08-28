from binance.spot import Spot
import api
import yfinance as yf
import matplotlib.pyplot as plt
import TechnicalIndicators as TA
import Signals as S
import time
import datetime as dt
import numpy as np
import pandas as pd

# Initialize Binance spot
client = Spot()
client = Spot(key=api.Binance, secret=api.BinanceSecret)

# Converts Binance candlestick data to pandas DataFrame format with correct types and formatted date
def klines_df(Ticker,Time,lim):
    A = client.klines(Ticker,Time,limit=lim)
    for row in A:
        for item in row:
            item = float(item)
        row[0] = dt.datetime.fromtimestamp(float(row[0])/1000)
        for _ in range(6):
            row.pop()
    c = ["Time","Open","High","Low","Close","Volume"]
    df = pd.DataFrame(data=A,columns=c)
    df.Open = df.Open.astype(float)
    df.High = df.High.astype(float)
    df.Low = df.Low.astype(float)
    df.Close = df.Close.astype(float)
    df.Volume = df.Volume.astype(float)
    return df

# Updates existing candlestick data from data/TickerTime.csv
def update(Ticker,Time):
    filename = "data/" + str(Ticker) + str(Time)
    try:
        df = pd.read_csv(filename + ".csv")
        last_time = df.Time.to_list()[-1]
    except:
        udf = klines_df(Ticker,Time,1000)
        udf.to_csv(filename + ".csv")
        return -1
    last_time = dt.datetime.strptime(last_time,'%Y-%m-%d %H:%M:%S')
    udf = klines_df(Ticker,Time,1000)
    udf = udf[udf["Time"] > last_time]
    if (len(udf) == 0): # Nothing to update, so exit
        return -1
    df = df.append(udf)
    df["Index"] = [i for i in range(0,len(df))]
    df.set_index(df.Index,inplace=True)
    df = df.drop("Index",axis=1)
    df.to_csv(filename + ".csv")
    return df

if __name__ == "__main__":
    sec = 900
    start_time = time.time()
    Tickers = ["BTCUSDT","ETHUSDT","ICXUSDT"]
    Times = ["1d","1h","5m","1m"]
    U = []
    i = 0
    while (True):
        for ticker in Tickers:
            for t in Times:
                df = update(ticker,t)
                if (type(df) != type(-1)):
                    U.append(ticker + t)
        print("Iteration", i, "\tupdated:", U)
        U = []
        i += 1
        time.sleep(sec - ((time.time() - start_time) % sec))
