from iqoptionapi.stable_api import IQ_Option
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from joblib import dump
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
goal="EURUSD"
i=0
X = []
Y = []
Mqtd = 100000
qtd = 67
while i < Mqtd * qtd:
    candles = iq.get_candles(goal,1,qtd,time.time() - i)
    opens = get_opens(candles[0:7])
    open = candles[6]['open']
    close = candles[-1]['close']
    minimum = get_min(candles[0:7])
    maximum = get_max(candles[0:7])
    volume = get_volumes(candles[0:7])
    if open > close:
        Y.append(-1)
        X.append([open,opens,minimum,maximum,volume])
    elif close > open:
        Y.append(1)
        X.append([open,opens,minimum,maximum,volume])
    i+=qtd
    print(f"At {i}")
scaler = StandardScaler()

clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(100,), random_state=1,max_iter=1000000)
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=42)
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)
clf.fit(X_train, y_train)
dump(clf, 'NNtest3.joblib') 
dump(scaler, 'scaler.joblib')

'''iq = IQ_Option("YOUR_EMAIL","YOUR_PASSWORD")
iq.connect()
goal="EURUSD"
candles = iq.get_candles(goal,1,1000,time.time())
df = pd.DataFrame(candles)
df.drop(columns=['from','id','at','to'],inplace=True)
print(df)
df.to_csv('iq.csv',index=False)'''

print(clf.score(X_test,y_test))
