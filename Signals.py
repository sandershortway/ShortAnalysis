import numpy as np
import TechnicalIndicators as TA
# Buy = -1, Sell = -1

def RSI(df,n):
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
    
def BB(df,n,m):
    df = TA.BB(df,n,m)
    P = df.Open.to_list()
    H = df.BBhigh.to_list()
    L = df.BBlow.to_list()
    S = []
    for i in range(0,len(P)):
        if (P[i] <= L[i]):
            S.append(-1)
        elif (P[i] >= H[i]):
            S.append(1)
        else:
            S.append(0)
    df["BBsignal"] = S
    return df.BBsignal

def eMA(df,n):
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
