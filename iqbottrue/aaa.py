from joblib import load
from training import prep_data
import pickle
import numpy as np


clf = load("model2.joblib")

with open("x_dump.dat", 'rb') as f:
    x = pickle.load(f)

with open("y_dump.dat", 'rb') as f:
    y = pickle.load(f)
    
print(clf.score(x, y))

"""
y = y.tolist()
i = 0
for inp in x:
    pred = clf.predict_proba([inp])[0]
    up = pred[1]
    down = pred[0]
    #print(pred)
    

    if up > 0.7 or down > 0.7:
        print(pred,  y[i])
        pass
    i+=1


"""