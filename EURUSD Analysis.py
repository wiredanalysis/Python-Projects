import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from sklearn.linear_model import LinearRegression
import seaborn as sns

# Set up API key and endpoint
api_key = "G5VBBZPVHKYBKOX6"
symbol = "USD"
base_url = "https://www.alphavantage.co/query"

# Construct API request URL
params = {
    "function": "FX_DAILY",
    "from_symbol": symbol,
    "to_symbol": "EUR",
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
df["EUR/USD Exchange Rate"] = 1 / df["close"]


# Analyze currency trends
plt.plot(df.index[-90:], df["EUR/USD Exchange Rate"].tail(90))
plt.xlabel("Date")
plt.ylabel("EUR/USD Exchange Rate")

# Use AutoDateLocator and DateFormatter to adjust tick frequency and format dates
date_fmt = mdates.DateFormatter('%Y-%m-%d')
plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
plt.gca().xaxis.set_major_formatter(date_fmt)
plt.gcf().autofmt_xdate()

plt.show()

  # Define rolling window and calculate moving average
rolling_window = 30
df["Moving Average"] = df["EUR/USD Exchange Rate"].rolling(rolling_window).mean()

# Predict exchange rate for next 30 days using moving average
last_date = df.index[-1]
prediction_dates = pd.date_range(last_date + pd.Timedelta(days=1), periods=29, freq="D")
predictions = df["Moving Average"].iloc[-1:].repeat(29).reset_index(drop=True)

# Visualize actual and predicted exchange rates for last 90 days and next 30 days
last_90_days = df["EUR/USD Exchange Rate"].tail(90)
last_90_days_index = last_90_days.index
plt.plot(last_90_days_index, last_90_days, label="Actual")
plt.plot(prediction_dates, predictions, label="Predicted")
plt.xlabel("Date")
plt.ylabel("EUR/USD Exchange Rate")
plt.legend()
plt.show()

# Calculate daily returns for last 180 days
daily_returns = df['EUR/USD Exchange Rate'].tail(180).pct_change()

# Plot daily returns over time
fig, ax = plt.subplots()
ax.plot(daily_returns.index, daily_returns)
ax.set_xlabel('Date')
ax.set_ylabel('Daily Returns')
ax.set_title('EUR/USD Daily Returns (Last 180 Days)')
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
ax.xaxis.set_tick_params(rotation=0)

plt.show()

# Construct API request URL
params = {
    "function": "FX_INTRADAY",
    "from_symbol": symbol,
    "to_symbol": "EUR",
    "apikey": api_key,
    "interval": "15min",
    "outputsize": "full"
}
response = requests.get(base_url, params=params)


# Convert response data to DataFrame
data = response.json()
df = pd.DataFrame.from_dict(data["Time Series FX (15min)"], orient="index")
df.index = pd.to_datetime(df.index)
df = df.sort_index()
df.columns = ["open", "high", "low", "close"]
df["close"] = pd.to_numeric(df["close"])

# Calculate short-term (50) and long-term (200) simple moving averages
short_term = 50
long_term = 200
df["SMA_short"] = df["close"].rolling(window=short_term).mean()
df["SMA_long"] = df["close"].rolling(window=long_term).mean()

# Create signals for buy and sell based on SMA crossover
df["Signal"] = np.where(df["SMA_short"] > df["SMA_long"], "Buy", "Sell")


# Visualize the buy and sell signals using different colors
plt.plot(df.index, df["close"], label="EUR/USD Exchange Rate")
plt.plot(df.index, df["SMA_short"], label=f"{short_term}-day SMA")
plt.plot(df.index, df["SMA_long"], label=f"{long_term}-day SMA")
plt.scatter(df[df["Signal"] == "Buy"].index, df[df["Signal"] == "Buy"]["close"], color="green", marker="^", label="Buy Signal")
plt.scatter(df[df["Signal"] == "Sell"].index, df[df["Signal"] == "Sell"]["close"], color="red", marker="v", label="Sell Signal")
plt.xlabel("Date")
plt.ylabel("EUR/USD Exchange Rate")
plt.legend()
plt.show()