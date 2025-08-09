from iqoptionapi.stable_api import IQ_Option
from numpy import NaN
from joblib import load
import time

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
p = 0
money = None

scaler = load('scaler.joblib')
clf = load('NNtest3.joblib')

while True:
    t = time.localtime(time.time())
    if t.tm_sec > 2 and t.tm_sec < 4:
        if money == iq.get_balance():
            p+=1
        elif p != 0:
            p -= 0
        if p >= 3:
            print("Pausing")
            time.sleep(600)
            p = 0
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
            money = iq.get_balance()
        if pred[0][1] > 0.999:
            check, id = iq.buy(1,goal,'put',1)
            money = iq.get_balance()
        time.sleep(60)
