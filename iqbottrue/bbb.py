from joblib import load
from training import prep_data
import pickle
import numpy as np


clf = load("model.joblib")
clf2= load("model2.joblib")
clf3 = load("model3.joblib")
clf4 = load("model4.joblib")


with open("data.dat", 'rb') as f:
    data = pickle.load(f)

x,y = prep_data(data[:1000])
y = y.tolist()
i = 0
c = 0
e = 0
for inp in x:
    pred = clf.predict([inp])[0]

    pred2 = clf2.predict([inp])[0]

    pred3 = clf3.predict([inp])[0]

    pred4 = clf4.predict([inp])[0]
    #print(pred)

    if pred == 1 and pred2 == 1:
        if y[i] == 1:
            c +=1
        else:
            e +=1
    if pred == -1 and pred2 == -1:
        if y[i] == -1:
            c +=1
        else:
            e +=1

    i+=1

print(c, e, c+e)