from training import prep_data
from iqoptionapi.stable_api import IQ_Option
import time
from joblib import load


iq = IQ_Option("YOUR_EMAIL","YOUR_PASSWORD")
iq.connect()
clf = load("model.joblib")
clf2 = load("model3.joblib")

while True:
    t = time.localtime(time.time())
    if t.tm_sec > 57:
        candle = iq.get_candles("EURUSD", 60, 2, time.time())
        candle0 = candle[0]
        candle1 = candle[1]
        minmaxopen = (candle0["max"] - candle0["open"]) / (candle0["max"] - candle0["min"])
        minmaxclose = (candle0["max"] - candle0["close"]) / (candle0["max"] - candle0["min"])

        minmaxopen1 = (candle1["max"] - candle1["open"]) / (candle1["max"] - candle1["min"])
        minmaxclose1 = (candle1["max"] - candle1["close"]) / (candle1["max"] - candle1["min"])
        x = [[minmaxopen, minmaxclose, minmaxopen1, minmaxclose1]]
        pred = clf.predict_proba(x)[0]
        pred2 = clf2.predict_proba(x)[0]
        print(pred, pred2)

        if pred[0] > 0.5 and pred2[0] > 0:
            print("aaa")
            check, id = iq.buy(1,"EURUSD",'put',1)
        elif pred[1] > 0.5 and pred2[1] > 0:
            print("BBBB")
            check, id = iq.buy(1,"EURUSD",'call',1)

        time.sleep(10)
        