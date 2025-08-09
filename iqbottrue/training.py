import pickle
import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
import numpy as np
from joblib import dump
import traceback


def prep_data(data):
    closes = {}
    mival = {}
    maxval = {}
    opens = {}

    for dot in data[:490000]:
        closes[dot["from"]] = dot["close"]
        mival[dot["from"]] = dot["min"]
        maxval[dot["from"]] = dot["max"]
        opens[dot["from"]] = dot["open"]

    df = pd.DataFrame({"time": closes.keys(), "close": closes.values(), "open":opens.values(),"minval": mival.values(), "maxval": maxval.values()})
    df["shift"] = df["close"].shift(-1)
    df["minmaxopen"] = (df["maxval"]-df["open"])/(df["maxval"]-df["minval"])
    df["minmaxclose"] = (df["maxval"]-df["close"])/(df["maxval"]-df["minval"])
    df["updown"] = df["close"] - df["open"] 
    print(df.head(10))
    #df.plot(x='time', y='perct')
    #plt.show()
    df.dropna(inplace=True)
    samples = []
    sample = []
    updowns = []
    hist = []
    ydown = []
    yup = []
    yzero = []

    for index, row in df.iterrows():
        y = 3
        updowns.append(row.iloc[-1])
        hist.append([row.iloc[-3], row.iloc[-2]])

        if len(updowns) == 2:
            if updowns[-2] < 0 and (updowns[-1] > (updowns[-2]*0.1)*-1 and updowns[-1] > 0):
                for h in hist:
                    sample.append(h[0])
                    sample.append(h[1])
                updowns = []
                hist = []
            elif updowns[-2] > 0 and (updowns[-1] < (updowns[-2]*0.1)*-1 and updowns[-1] < 0):
                for h in hist:
                    sample.append(h[0])
                    sample.append(h[1])
                updowns = []
                hist = []
            else:
                updowns = []
                hist = []
                sample = []
                continue

            if row.iloc[2] > row.iloc[1]:
                        y = -1
                        ydown.append(1)
            elif row.iloc[2] < row.iloc[1]:
                        y = 1
                        yup.append(1)

            if y != 3:
                samples.append({"x": sample, "y": y})
            sample = []
    
    
    values = pd.DataFrame(samples)
    print(values["y"].value_counts())
    values["y"] = values["y"].shift(-1)
    values.dropna(inplace=True)

    #print(values.head(10))
    #print(values.tail(10))
    print(values["y"].value_counts())
    
    X = np.array(values["x"].to_list())
    
    
    return X, values["y"]

def train():
    with open("data.dat", 'rb') as f:
        data = pickle.load(f)

    x,y = prep_data(data)

    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.1,random_state=1)

    "{'lbfgs, sgd, adam}"
 
    #clf = SVC(kernel="rbf", gamma="auto",max_iter=1000, C=0.001, probability=True)
    clf = MLPClassifier(hidden_layer_sizes=(10,20,30), max_iter=1000, learning_rate="constant", solver="adam", verbose=True, alpha=1e-1, tol=1e-6)
    clf.fit(X_train, y_train)

    print(clf.score(X_test, y_test))
    dump(clf, 'model.joblib')

if __name__ == "__main__":
    train()

'''

            if close[0] > close[-1]:
                y = -1
            elif close[0] < close[-1]:
                y = 1
            else:
                sample = []
                close = []
                continue
                
            '''