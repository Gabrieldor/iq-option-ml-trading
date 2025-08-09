from datetime import datetime
import time
import matplotlib.pyplot as plt
from random import randint, uniform
import pandas as pd
import traceback
import pickle


now = int(time.time())
size = 1500
candle_size = 5
samples = []



for x in range(now, now-(size*candle_size), -candle_size):
    try:
        y = (samples[-1]["close"] + samples[-2]["close"]  + samples[-3]["close"]) / randint(2,6) 
    except:
        #print(traceback.format_exc())
        y = randint(10, 50)

    samples.append({"from": x, "close": y})

with open("data.dat", "wb") as f:
    pickle.dump(samples, f)
    pass

df = pd.DataFrame(samples)
df.plot(x='from', y='close')
plt.show()




