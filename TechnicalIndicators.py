import numpy as np

# Average True Range
def ATR(DF,n):
    df = DF.copy()
    df['H-L']=abs(df['High']-df['Low'])
    df['H-PC']=abs(df['High']-df['Close'].shift(1))
    df['L-PC']=abs(df['Low']-df['Close'].shift(1))
    df['TR']=df[['H-L','H-PC','L-PC']].max(axis=1,skipna=False)
    df['ATR'] = df['TR'].rolling(n).mean()
    df2 = df.drop(['H-L','H-PC','L-PC'],axis=1)
    return df2

# Moving Average Convergence Divergence
def MACD(DF,x,y,z):
    df = DF.copy()
    df["MA_Fast"] = df.Open.ewm(span=x,min_periods=x).mean()
    df["MA_Slow"] = df.Open.ewm(span=y,min_periods=y).mean()
    df["MACD"] = df["MA_Fast"] - df["MA_Slow"]
    df["Signal"] = df["MACD"].ewm(span=z,min_periods=z).mean()
    df.dropna(inplace=True)
    return df
    
# Simple Moving Average
def sMA(DF,n):
    df = DF.copy()
    df["sMA"] = df["Close"].rolling(n).mean()
    return df.sMA

# Weighted Moving Average
def wMA(DF,n):
    df = DF.copy()
    n = round(n)
    P = df["Close"].to_list()
    W = []
    d = n * (n+1) / 2
    for i in range(0,len(df)):
        w = 0
        v = 1
        if (i < n - 1):
            W.append(np.nan)
        else:
            for j in range(i - n + 1, i + 1):
                w += v * P[j]
                v += 1
            W.append(w/d)
    df["wMA"] = W
    return df.wMA

# Hull Moving Average
def HullMA(DF,n):
    df = DF.copy()
    df["wMA1"] = 2 * wMA(df,n/2) - wMA(df,n)
    P = df["wMA1"].to_list()
    n = round(np.sqrt(n))
    W = []
    d = n * (n+1) / 2
    for i in range(0,len(df)):
        w = 0
        v = 1
        if (i < n - 1):
            W.append(np.nan)
        else:
            for j in range(i - n + 1, i + 1):
                w += v * P[j]
                v += 1
            W.append(w/d)
    df["HullMA"] = W
    return df.HullMA

# Difference from sMA normalized in std's
def NormDiffsMA(DF,n):
    df = DF.copy()
    df["sMA"] = df["Close"].rolling(n).mean()
    df["Diff"] = df["Close"] - df["sMA"]
    df["sMADiffPerc"] = df["Diff"] / df["Diff"].std()
    df.dropna(inplace=True)
    df = df.drop(["sMA","Diff"],axis=1)
    return df.sMADiffPerc

# Simple Moving Average Crossover
def sMAcross(DF,n):
    df = DF.copy()
    df = sMA(DF,n)
    df["MAcross"] = np.where(np.logical_or(np.logical_and(df["Open"]>df["sMA"],df["Close"]<df["sMA"]),np.logical_and(df["Open"]<df["sMA"],df["Close"]>df["sMA"])),True,False)
    return df

# Exponential Moving Average
def eMA(DF,n):
    df = DF.copy()
    df["eMA"] = df["Close"].ewm(span=n,adjust=False).mean()
    return df.eMA

# Exponential Moving Average Crossover
def eMAcross(DF,n):
    df = DF.copy()
    df = eMA(DF,n)
    df["MAcross"] = np.where(np.logical_or(np.logical_and(df["Open"]>df["eMA"],df["Close"]<df["eMA"]),np.logical_and(df["Open"]<df["eMA"],df["Close"]>df["eMA"])),True,False)
    return df

# Bollinger Bands
def BB(DF,n,m):
    df = DF.copy()
    df["MA"] = df["Open"].rolling(n).mean()
    df["BBhigh"] = df["MA"] + m * df["MA"].rolling(n).std()
    df["BBlow"] = df["MA"] - m * df["MA"].rolling(n).std()
    df.dropna(inplace=True)
    df.drop("MA",axis=1)
    return df

# Exponential Bollinger Bands
def eBB(DF,n,m):
    df = DF.copy()
    df["MA"] = eMA(df,n)
    df["BBhigh"] = df["MA"] + m * df["MA"].rolling(n).std()
    df["BBlow"] = df["MA"] - m * df["MA"].rolling(n).std()
    df.dropna(inplace=True)
    return df

# Golden Cross (n period MA and m period MA cross, n > m)
def GoldCross(DF,n,m):
    df = DF.copy()
    df["nMA"] = sMA(DF,n).sMA
    df["mMA"] = sMA(DF,m).sMA
    df["Diff"] = df["nMA"] - df["mMA"]
    df["GoldCrossSell"] = np.where(np.logical_and(df["Diff"]>=0,df["Diff"].shift(-1)<0),True,False)
    df["GoldCrossBuy"] = np.where(np.logical_and(df["Diff"]<=0,df["Diff"].shift(-1)>0),True,False)
    sell = df.GoldCrossSell.to_list()
    buy = df.GoldCrossBuy.to_list()
    GCsignal = []
    for i in range(0,len(sell)):
        if (sell[i]):
            GCsignal.append("Sell")
        elif (buy[i]):
            GCsignal.append("Buy")
        else:
            GCsignal.append("None")
    df["GoldCross"] = GCsignal
    return df.GoldCross

# Relative Strength Index
def RSI(DF,n):
    df = DF.copy()
    df["Delta"] = df["Close"] - df["Close"].shift(1)
    # df.drop("Delta",axis = 1, inplace = True)
    df["Gain"] = np.where(df["Delta"] >= 0, df["Delta"], 0)
    df["Loss"] = np.where(df["Delta"] < 0, -df["Delta"], 0)
    Gain = df["Gain"].to_list()
    Loss = df["Loss"].to_list()
    # df.drop("Gain",axis = 1, inplace = True)
    # df.drop("Loss",axis = 1, inplace = True)
    AvgGain = []
    AvgLoss = []
    
    for i in range(0,len(df)):
        if (i < n):
            AvgGain.append(np.NaN)
            AvgLoss.append(np.NaN)
        elif (i == n):
            AvgGain.append(df["Gain"].rolling(n).mean().to_list()[-1])
            AvgLoss.append(df["Loss"].rolling(n).mean().to_list()[-1])
        elif (i > n):
            AvgGain.append(((n-1)*AvgGain[i-1] + Gain[i])/n)
            AvgLoss.append(((n-1)*AvgLoss[i-1] + Loss[i])/n)
    
    df["AvgGain"] = np.array(AvgGain)
    df["AvgLoss"] = np.array(AvgLoss)
    df["RS"] = df["AvgGain"] / df["AvgLoss"]
    df["RSI"] = 100 - (100/(1+df["RS"]))
    # df.drop("Delta",axis = 1, inplace = True)
    return df

# Average Directional Index
def ADX(DF,n):
    df2 = DF.copy()
    df2['TR'] = ATR(df2,n)['TR']
    df2['DMplus']=np.where((df2['High']-df2['High'].shift(1))>(df2['Low'].shift(1)-df2['Low']),df2['High']-df2['High'].shift(1),0)
    df2['DMplus']=np.where(df2['DMplus']<0,0,df2['DMplus'])
    df2['DMminus']=np.where((df2['Low'].shift(1)-df2['Low'])>(df2['High']-df2['High'].shift(1)),df2['Low'].shift(1)-df2['Low'],0)
    df2['DMminus']=np.where(df2['DMminus']<0,0,df2['DMminus'])
    TRn = []
    DMplusN = []
    DMminusN = []
    TR = df2['TR'].tolist()
    DMplus = df2['DMplus'].tolist()
    DMminus = df2['DMminus'].tolist()
    for i in range(len(df2)):
        if i < n:
            TRn.append(np.NaN)
            DMplusN.append(np.NaN)
            DMminusN.append(np.NaN)
        elif i == n:
            TRn.append(df2['TR'].rolling(n).sum().tolist()[n])
            DMplusN.append(df2['DMplus'].rolling(n).sum().tolist()[n])
            DMminusN.append(df2['DMminus'].rolling(n).sum().tolist()[n])
        elif i > n:
            TRn.append(TRn[i-1] - (TRn[i-1]/n) + TR[i])
            DMplusN.append(DMplusN[i-1] - (DMplusN[i-1]/n) + DMplus[i])
            DMminusN.append(DMminusN[i-1] - (DMminusN[i-1]/n) + DMminus[i])
    df2['TRn'] = np.array(TRn)
    df2['DMplusN'] = np.array(DMplusN)
    df2['DMminusN'] = np.array(DMminusN)
    df2['DIplusN']=100*(df2['DMplusN']/df2['TRn'])
    df2['DIminusN']=100*(df2['DMminusN']/df2['TRn'])
    df2['DIdiff']=abs(df2['DIplusN']-df2['DIminusN'])
    df2['DIsum']=df2['DIplusN']+df2['DIminusN']
    df2['DX']=100*(df2['DIdiff']/df2['DIsum'])
    ADX = []
    DX = df2['DX'].tolist()
    for j in range(len(df2)):
        if j < 2*n-1:
            ADX.append(np.NaN)
        elif j == 2*n-1:
            ADX.append(df2['DX'][j-n+1:j+1].mean())
        elif j > 2*n-1:
            ADX.append(((n-1)*ADX[j-1] + DX[j])/n)
    df2['ADX']=np.array(ADX)
    return df2['ADX']

# On Balance Volume
def OBV(DF):
    df = DF.copy()
    df["Term"] = np.where(df["Close"].shift(1)>df["Close"],df["Volume"],-df["Volume"])
    df["OBV"] = df["Term"].cumsum()
    return df.OBV