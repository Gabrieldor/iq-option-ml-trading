import threading
from iqoptionapi.stable_api import IQ_Option
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from joblib import dump
import pandas as pd
from queue import Queue
from random import randint
import time


def dl(entry,q,iq):
    while q.empty() is False:
        i = q.get()
        candles = iq.get_candles(goal,secs,qtd,(time.time() - 345600) - i)
        for candle in candles:
            entry.append([candle["from"], candle["open"]])
        print(f"At {i}")

iq = IQ_Option("YOUR_EMAIL","YOUR_PASSWORD")
iq.connect()
iq.get_candles()

goal="EURJPY"
i = 0
z = 0
Mqtd = 100
secs = 10 
delay = 0
qtd = secs + delay
q = Queue(maxsize=Mqtd)
entry = []

while i < Mqtd * qtd:
    q.put(i)
    i+=qtd
    

dl(entry,q,iq)
time.sleep(3)
#print(entry)

df = pd.DataFrame(entry, columns=["A","B"])
df.to_csv("aaa.csv")
df.plot(x='A', y='B',)
plt.show()



"""
Y = df["B"]
X = df["A"].shift(300)
X.dropna(inplace=True)
Y = Y[300:]
X = X.to_numpy().reshape(-1, 1)

clf = LinearRegression()
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=42)
clf.fit(X_train, y_train)
dump(clf, 'model.joblib')

print(clf.score(X_test,y_test))

"""
