from iqoptionapi.stable_api import IQ_Option
import time
import pickle

now = time.time()
iq = IQ_Option("YOUR_EMAIL","YOUR_PASSWORD")
iq.connect()
dur = 300

def dl(time_max, range):
    global now, dur
    global iq
    return iq.get_candles("EURUSD", dur, range, now - time_max)

def dl_total(max, step):
    total = []

    for i in range(max, 0, -step):
        dl_arr = dl(i*dur, step)
        total += dl_arr[:len(dl_arr)-1]
        print(f"At: {i}")

    return total


    

total = dl_total(500000,1000)
with open("data.dat", "wb") as f:
        pickle.dump(total, f)