import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Set up API key and endpoint
api_key = "G5VBBZPVHKYBKOX6"
symbol = "EUR"
base_url = "https://www.alphavantage.co/query"

# Construct API request URL
params = {
    "function": "FX_DAILY",
    "from_symbol": symbol,
    "to_symbol": "USD",
    "apikey": api_key,
    "outputsize": "full"
}
response = requests.get(base_url, params=params)

# Convert response data to DataFrame
data = response.json()
df = pd.DataFrame.from_dict(data["Time Series FX (Daily)"], orient="index")
df.index = pd.to_datetime(df.index)
df = df.sort_index()
df.columns = ["open", "high", "low", "close"]
df["close"] = pd.to_numeric(df["close"])
df["USD/EUR Exchange Rate"] = 1 / df["close"]

# Analyze currency trends
plt.plot(df.index, df["USD/EUR Exchange Rate"])
plt.xlabel("Date")
plt.ylabel("USD/EUR Exchange Rate")
plt.show()

  #Make Predictive Module

import matplotlib.dates as mdates

# Split the data into training and testing sets
train_size = int(len(df) * 0.8)
train_df = df.iloc[:train_size]
test_df = df.iloc[train_size:]

# Create feature matrix X and target vector y for training data
X_train = np.array(range(len(train_df))).reshape(-1, 1)
y_train = train_df["USD/EUR Exchange Rate"].values

# Train a linear regression model on the training data
model = LinearRegression()
model.fit(X_train, y_train)

# Use the trained model to predict future exchange rates
X_test = np.array(range(len(train_df), len(df))).reshape(-1, 1)
y_pred = model.predict(X_test)

# Visualize the predicted exchange rates
fig, ax = plt.subplots()
ax.plot(test_df.index, test_df["USD/EUR Exchange Rate"], label="actual")
ax.plot(test_df.index, y_pred, label="predicted")
ax.set_xlabel("Date")
ax.set_ylabel("USD/EUR Exchange Rate")

# Format the date labels on the x-axis
date_format = mdates.DateFormatter('%m-%d-%Y')
ax.xaxis.set_major_formatter(date_format)
fig.autofmt_xdate()

plt.legend()
plt.show()




# Create feature matrix X for future predictions
X_future = np.array(range(len(df), len(df) + 30)).reshape(-1, 1)

# Use the trained model to predict exchange rates for the next 30 days
y_future = model.predict(X_future)

# Print the predicted exchange rates for the next 30 days
print("Predicted exchange rates for the next 30 days:")
print(y_future)



import matplotlib.dates as mdates

# Split the data into training and testing sets
train_size = int(len(df) * 0.8)
train_df = df.iloc[:train_size]
test_df = df.iloc[train_size:]

# Create feature matrix X and target vector y for training data
X_train = np.array(range(len(train_df))).reshape(-1, 1)
y_train = train_df["USD/EUR Exchange Rate"].values

# Train a linear regression model on the training data
model = LinearRegression()
model.fit(X_train, y_train)

# Use the trained model to predict exchange rates for the next 30 days
X_test = np.array(range(len(df), len(df) + 30)).reshape(-1, 1)
y_pred = model.predict(X_test)

# Visualize the predicted exchange rates for the next 30 days
fig, ax = plt.subplots()
ax.plot(range(1, 31), y_pred, label="predicted")
ax.set_xlabel("Days")
ax.set_ylabel("USD/EUR Exchange Rate")

plt.legend()
plt.show()
