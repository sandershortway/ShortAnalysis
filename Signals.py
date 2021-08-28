import numpy as np
import TechnicalIndicators as TA

def RSI(DF,n):
    df = DF.copy()
    df["RSI"] = TA.RSI(df,n).RSI
    R = df.RSI.to_list()
    S = []
    for r in R:
        if (r <= 30):
            S.append(-1)
        elif (r >= 70):
            S.append(1)
        else:
            S.append(0)
    df["RSIsignal"] = S
    return df.RSIsignal

def Offset(DF,n):
    df = DF.copy()
    P = df.Open.to_list()
    df["Avg"] = df.Open.rolling(n).mean()
    df["StdDev"] = df.Open.rolling(n).std()
    df["Offset"] = (df["Open"] - df["Avg"]) / df["StdDev"]
    return df.Offset

def eMA(DF,n):
    df = DF.copy()
    df["eMA"] = TA.eMA(df,n)
    df.dropna()
    S = []
    P = df.Close.to_list()
    MA = df.eMA.to_list()
    for i in range(0,len(P)):
        if (P[i] <= MA[i]):
            S.append(-1)
        elif (P[i] >= MA[i]):
            S.append(1)
    df["eMAsignal"] = S
    return df.eMAsignal