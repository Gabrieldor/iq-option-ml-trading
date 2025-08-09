from iqoptionapi.stable_api import IQ_Option
import numpy as np
import time
from sklearn import preprocessing
import pandas as pd


def get_opens(candles):
    open = []
    i=0
    while i < len(candles):
        open.append(candles[i]['open'])
        i+=1
    return open

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
    volumes = 0
    i=1
    while i < len(candles):
        diff = candles[i]['volume'] - candles[i-1]['volume']
        volumes = volumes + (diff * abs(diff)/i)
        i+=1    
    return volumes

iq = IQ_Option("YOUR_EMAIL","YOUR_PASSWORD")
iq.connect()
goal="EURJPY-OTC"
delay = 45
p = 0
money = None
testclose = 999999
call = None
check = None
win = 0
lose = 0
loaded_models = [load_model(f'clf_{x}') for x in range(0, 10)]
print(loaded_models)

while True:
    t = time.localtime(time.time())
    if t.tm_sec < 2:
        id = None
        print(testclose, iq.get_candles(goal,1,1,time.time())[0]['close'])
        if call == 0:
            if wl != -1:
                win+=1
            else:
                lose+=1
                
        
        if call == 1:
            if wl != -1:
                win+=1
            else:
                lose+=1
        print(f"win {win}", lose)
            
        call = None
        candles = iq.get_candles(goal,1,delay+1,time.time())
        opens = get_opens(candles)
        df = pd.DataFrame(opens, columns=["A"])
        df['A'] = df["A"].pct_change()
        df.drop(index=0, inplace = True)
        X = np.array(df["A"].to_list())
        X = X.reshape(1,1,45)
        
        pred = [model.predict(X)[0] for model in loaded_models]
        up = [x[0][0] for x in pred]
        down = [x[0][1] for x in pred]
        print(up, down, pred)
        if sum(up) > sum(down):
            testclose = iq.get_candles(goal,1,1,time.time())[0]['close']
            check, id = iq.buy(1,goal,'call',0.5)
            call = 0
            print("sobe")
        elif sum(down) > sum(up): 
            testclose = iq.get_candles(goal,1,1,time.time())[0]['close']
            check, id = iq.buy(1,goal,'put',0.5)
            call = 1
            print("desce")
        if id != None:
            wl = iq.check_win_v3(id)
