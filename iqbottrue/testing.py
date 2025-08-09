from iqoptionapi.stable_api import IQ_Option
import time
from joblib import load


iq = IQ_Option("YOUR_EMAIL","YOUR_PASSWORD")
iq.connect()
clf = load("model.joblib")

while True:
    t = time.localtime(time.time())
    if t.tm_sec > 1 and t.tm_sec < 3:
        candle = iq.get_candles("EURUSD", 60, 2, time.time())
        candle0 = candle[0]
        minmaxopen = (candle0["max"] - candle0["open"]) / (candle0["max"] - candle0["min"])
        minmaxclose = (candle0["max"] - candle0["close"]) / (candle0["max"] - candle0["min"])
        print(minmaxopen, minmaxclose)

        x = [[minmaxopen, minmaxclose]]
        print(clf.predict(x))
        pred = clf.predict_proba(x)[0]
        print(pred)

        if pred[0] > 0.5:
            print("aaa")
            check, id = iq.buy(1,"EURUSD",'put',1)
        elif pred[-1] > 0.5:
            print("BBBB")
            check, id = iq.buy(1,"EURUSD",'call',1)

        time.sleep(10)
        