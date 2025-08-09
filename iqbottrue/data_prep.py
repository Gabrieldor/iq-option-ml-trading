import pickle
import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose
import matplotlib.pyplot as plt



with open("data.dat", 'rb') as f:
    data = pickle.load(f)

print(data)

closes = {}
for dot in data:
    closes[dot["from"]] = dot["close"]

df = pd.DataFrame({"time": closes.keys(), "close": closes.values()})
df.set_index("time", inplace=True)
df.sort_index(inplace=True)

df.plot(y='close', use_index=True)



plt.show()
    