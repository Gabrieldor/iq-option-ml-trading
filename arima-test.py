from iqoptionapi.stable_api import IQ_Option
import matplotlib.pyplot as plt
import time
import pandas as pd
from pandas.plotting import autocorrelation_plot
from statsmodels.tsa.arima.model import ARIMA
from pmdarima import auto_arima
import warnings 
warnings.filterwarnings("ignore") 


def arima(iq):
    data = []
    size = 60
    while len(data) < 1:
        if len(data) == 0:
            now = time.time()
        info = iq.get_candles("EURUSD-OTC", size, 120 + 1, now)
        now = info[0]["from"] - size
        for i in info[::-1]:
            data.append({"x": i["from"], "y": i["close"]*1000})

    df = pd.DataFrame(data[::-1])
    print(df)
    input()
    df["shift"] = df["y"].shift(-1)
    df.dropna(inplace=True)
    """stepwise_fit = auto_arima(df['y'], start_p = 1, start_q = 1, 
                            max_p = 3, max_q = 3, m = 1, 
                            start_P = 0, seasonal = False, 
                            d = None, D = 1, trace = True, 
                            error_action ='ignore',   # we don't want to know if an order does not work 
                            suppress_warnings = True,  # we don't want convergence warnings 
                            stepwise = True)"""
    #
    model = ARIMA(df["y"].diff(), order=(3,0,0))
    result = model.fit()
    pred = result.forecast(steps=1)
    print('\n')
   #autocorrelation_plot(df["y"])
    print(pred[120], df["y"].diff().iloc[-1])
    if pred[120] > df["y"].diff().iloc[-1]*1.25:
        print("COMPRAAAAAAAAAAAAAAAAAAAA")
        return 1
    elif pred[120] < df["y"].diff().iloc[-1]*0.75:
        print("VENDEEEEEEEEEEEEEEE")
        return 0
    


iq = IQ_Option("YOUR_EMAIL","YOUR_PASSWORD")
iq.connect()

while True:
    t = time.localtime(time.time())
    if t.tm_sec < 55:
        id = None
        call = None
        pred = arima(iq)

        if pred == 1:
            check, id = iq.buy(5,"EURUSD-OTC",'call',1)
            call = 0
            print("sobe")
        elif pred == 0: 
            check, id = iq.buy(5,"EURUSD-OTC",'put',1)
            call = 1
            print("desce")

        time.sleep(5)



#df.plot(x="x", y="y")
#
