from iqoptionapi.stable_api import IQ_Option
from numpy import NaN
from joblib import load
import time

'''
candles = iq.get_candles(goal,5,1000,time.time())
df = pd.DataFrame(candles)
df.drop(columns=['from','id','at','to'],inplace=True)
pred = []
scaler = StandardScaler()
for index, row in df.iterrows():
    open = row['open']
    close = row['close']
    if open > close:
        pred.append(-1)
    elif close > open:
        pred.append(1)
    else:
        pred.append(0)

df.drop(columns=['close'],inplace=True)
df = df.assign(pred=pred)


Y = df.loc[:,'pred']
scaler.fit(X)
X = scaler.transform(X)
clf = load('NNtest.joblib')

print(clf.score(X,Y))'''

def get_opens(candles):
    open = []
    for candle in candles:
        open.append(candle['open'])
    return sum(open)/len(open)

def get_max(candles):
    maxs = []
    for candle in candles:
        maxs.append(candle['max'])
    return max(maxs)

def get_min(candles):
    mins = []
    for candle in candles:
        mins.append(candle['min'])
    return min(mins)

def get_volumes(candles):
    volumes = []
    for candle in candles:
        volumes.append(candle['volume'])
    return sum(volumes)/len(volumes)




iq = IQ_Option("YOUR_EMAIL","YOUR_PASSWORD")
iq.connect()
goal="EURUSD-OTC"

scaler = load('scaler.joblib')
clf = load('NNtest3.joblib')

while True:
    t = time.localtime(time.time())
    if t.tm_sec < 2:
        candles = iq.get_candles(goal,1,7,time.time())
        opens = get_opens(candles[0:7])
        open = candles[6]['open']
        close = candles[-1]['close']
        minimum = get_min(candles[0:7])
        maximum = get_max(candles[0:7])
        volume = get_volumes(candles[0:7])
        X = [[open,opens,minimum,maximum,volume]]
        X = scaler.transform(X)
        pred = clf.predict_proba(X)
        print(pred)
        if pred[0][0] > 0.999:
            check, id = iq.buy(1,goal,'call',1)
        if pred[0][1] > 0.999:
            check, id = iq.buy(1,goal,'put',1)
        time.sleep(60)
