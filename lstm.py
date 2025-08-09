from iqoptionapi.stable_api import IQ_Option
import matplotlib.pyplot as plt
import time
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
import numpy as np
import gym
from gym import spaces
from gym.utils import seeding


iq = IQ_Option("YOUR_EMAIL","YOUR_PASSWORD")
iq.connect()
data = []
size = 60
while len(data) < 50000:
    if len(data) == 0:
        now = time.time()
    info = iq.get_candles("EURUSD-OTC", size, 1000 + 1, now)
    now = info[0]["from"] - size
    for i in info[::-1]:
        data.append({"x": i["from"], "y": i["close"]})

df = pd.DataFrame(data[::-1])
df['target'] = (df['y'].shift(-1) > df['y']).astype(int)

# Feature Engineering: Use lagged values of y
df['lag_1'] = df['y'].shift(1)  # y(t-1)
df['lag_2'] = df['y'].shift(2)  # y(t-2)
df['lag_3'] = df['y'].shift(3)  # y(t-3)

# Drop rows with NaN values due to lagged features
df = df.dropna()

# Features and Target
X = df[['y', 'lag_1', 'lag_2', 'lag_3']]
y = df['target']

# Split the data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

class PredictDirectionEnv(gym.Env):
    def __init__(self, data, lags=3):
        super(PredictDirectionEnv, self).__init__()
        self.data = data
        self.lags = lags
        
        # Create states from the data
        self.features = X
        self.states = self.features.dropna().values
        self.targets = y

        self.current_step = 0
        self.action_space = spaces.Discrete(2)  # Two actions: predict up (1) or down (0)
        self.observation_space = spaces.Box(
            low=-np.inf, high=np.inf, shape=(lags + 1,), dtype=np.float32
        )

    def _create_features(self, data, lags):
        features = pd.DataFrame(data, columns=["y"])
        for lag in range(1, lags + 1):
            features[f"lag_{lag}"] = data.shift(lag)
        return features

    def reset(self):
        self.current_step = 0
        return self.states[self.current_step]
    
    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self, action):
        if self.current_step >= len(self.targets) - 1:
            done = True
            next_state = None
            reward = 0  # No reward as the episode is done
        else:
            correct_action = self.targets[self.current_step]
            reward = 1 if action == correct_action else -1
            self.current_step += 1

            done = self.current_step >= len(self.states) - 1
            next_state = self.states[self.current_step] if not done else None
            return next_state, reward, done, {}

    def render(self, mode="human"):
        pass

from stable_baselines3 import DQN
from stable_baselines3.common.env_util import make_vec_env

# Prepare the environment
data = df['y'].values
env = PredictDirectionEnv(data)
vec_env = make_vec_env(lambda: env, n_envs=1)

# Train the DQN agent
model = DQN("MlpPolicy", vec_env, verbose=1)
model.learn(total_timesteps=10000)

# Evaluate the agent
state = env.reset()
total_reward = 0
while True:
    action, _ = model.predict(state, deterministic=True)
    state, reward, done, _ = env.step(action)
    total_reward += reward
    if done:
        break

print("Total Reward:", total_reward)

input()
old_pred = None
# Make predictions

while True:
    t = time.localtime(time.time())
    if t.tm_sec < 5:
        id = None
        call = None
        now = time.time()
        data = []
        info = iq.get_candles("EURUSD-OTC", size, 5, now)
        for i in info[::-1]:
            data.append({"x": i["from"], "y": i["close"]})

        df = pd.DataFrame(data[::-1])

        y = np.array([df["y"]])
        y = np.reshape(y, (y.shape[0], y.shape[1], 1))
        predictions = "a"
        if old_pred != None:
            y = old_pred
        else:
            old_pred = predictions

        print(predictions, y)

        if predictions[0][0] > y[-1][0]:
            pred = 1
        else:
            pred = 0


        if pred == 1:
            check, id = iq.buy(5,"EURUSD-OTC",'call',1)
            call = 0
            print("sobe")
        elif pred == 0: 
            check, id = iq.buy(5,"EURUSD-OTC",'put',1)
            call = 1
            print("desce")

        time.sleep(35)