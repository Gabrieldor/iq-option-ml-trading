from iqoptionapi.stable_api import IQ_Option
import numpy as np
import time
import pandas as pd
from joblib import load

iq = IQ_Option("YOUR_EMAIL","YOUR_PASSWORD")
iq.connect()
goal="EURJPY"
delay = 45
p = 0
money = None
testclose = 999999
call = None
check = None
win = 0
lose = 0
clf = load("model.joblib")

while True:
    t = time.localtime(time.time())
    if t.tm_sec < 2:
        id = None
        call = None
        candles = iq.get_candles(goal,1,1,time.time())
        X = [[candles[0]["from"]]]
        op = [[candles[0]["open"]]]
        pred = clf.predict(X)
        print(pred)

        if pred > op:
            testclose = iq.get_candles(goal,1,1,time.time())[0]['close']
            check, id = iq.buy(1,goal,'call',5)
            call = 0
            print("sobe")
        elif pred < op: 
            testclose = iq.get_candles(goal,1,1,time.time())[0]['close']
            check, id = iq.buy(1,goal,'put',5)
            call = 1
            print("desce")

        time.sleep(5)
