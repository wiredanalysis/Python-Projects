import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates
from scipy.stats import norm
from scipy.stats import norm, normaltest
from datetime import datetime, timedelta
%matplotlib inline

# Load Apple's stock price data
apple = yf.Ticker("AAPL")
apple_data = apple.history(period="max")

# Visualize the stock price using a line plot and candlestick chart
plt.figure(figsize=(16,8))
plt.plot(apple_data['Close'])
plt.title("Apple Stock Price")
plt.xlabel("Date")
plt.ylabel("Stock Price ($)")
plt.show()

from mpl_finance import candlestick_ohlc
ohlc = apple_data[['Open', 'High', 'Low', 'Close']].reset_index()
ohlc['Date'] = ohlc['Date'].map(mdates.date2num)
plt.figure(figsize=(16,8))
ax = plt.subplot()
candlestick_ohlc(ax, ohlc.values, width=0.5, colorup='g', colordown='r', alpha=0.8)
plt.title("Apple Stock Price")
plt.xlabel("Date")
plt.ylabel("Stock Price ($)")
plt.show()

# Convert 'Date' column to datetime format and set as index
apple_data['Date'] = pd.to_datetime(apple_data['Date'])
apple_data.set_index('Date', inplace=True)

# Resample data to monthly frequency
apple_monthly = apple_data.resample('M').agg({'Open':'first', 'High':'max', 'Low':'min', 'Close':'last'})

# Create a range of dates with the desired frequency
date_range = pd.date_range(start=apple_data.index.min(), end=apple_data.index.max(), freq='M')

# Create a new column with the date range
apple_monthly['date_range'] = date_range

# Convert the date range to a format that can be used by candlestick_ohlc
ohlc = apple_monthly[['date_range', 'Open', 'High', 'Low', 'Close']].copy()
ohlc['date_range'] = ohlc['date_range'].map(mdates.date2num)

# Plot the candlestick chart
plt.figure(figsize=(16,8))
ax = plt.subplot()
candlestick_ohlc(ax, ohlc.values, width=0.5, colorup='g', colordown='r', alpha=0.8)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.title("Apple Stock Price")
plt.xlabel("Date")
plt.ylabel("Stock Price ($)")
plt.show()



# Calculate daily returns and plot cumulative returns
daily_returns = apple_data['Close'].pct_change().dropna()
cumulative_returns = (1 + daily_returns).cumprod() - 1
plt.figure(figsize=(16,8))
plt.plot(cumulative_returns)
plt.title("Apple Cumulative Returns")
plt.xlabel("Date")
plt.ylabel("Return (%)")
plt.show()

# Calculate and visualize the distribution of daily returns
plt.figure(figsize=(16,8))
sns.histplot(daily_returns, kde=True, stat='density')
plt.title("Apple Daily Returns Distribution")
plt.xlabel("Return (%)")
plt.show()
plt.figure(figsize=(16,8))
sns.kdeplot(daily_returns, bw_adjust=2)
plt.title("Apple Daily Returns Distribution")
plt.xlabel("Return (%)")
plt.show()

# Test for normality of the returns
alpha = 0.05
k2, p = norm.fit(daily_returns)
stat, pval = normaltest(daily_returns)
if pval < alpha:
    print("The daily returns do not follow a normal distribution.")
else:
    print("The daily returns follow a normal distribution.")

# Implement a Moving Average Crossover strategy and calculate profit/loss
ma50 = apple_data['Close'].rolling(window=50).mean()
ma200 = apple_data['Close'].rolling(window=200).mean()
apple_data['Signal'] = np.where(ma50 > ma200, 1, 0)
apple_data['Profit/Loss'] = apple_data['Signal'].shift(1) * apple_data['Close'].pct_change()
plt.figure(figsize=(16,8))
plt.plot(apple_data['Profit/Loss'].cumsum())
plt.title("Apple Moving Average Crossover Strategy")
plt.xlabel("Date")
plt.ylabel("Profit/Loss ($)")
plt.show()

# Examine correlation with the S&P 500
spy = yf.Ticker("^GSPC")
spy_data = spy.history(period="max")
apple_spy = pd.concat([apple_data['Close'], spy_data['Close']], axis=1, join="inner")
apple_spy.columns = ['Apple', 'S&P 500']
sns.scatterplot(data=apple_spy, x="S&P 500", y="Apple")
plt.title("Apple vs. S&P 500 Returns")
plt.xlabel("S&P 500 Returns")
plt.ylabel("Apple Returns")
plt.show()
corr = apple_spy.corr()

# Apple Monte Carlo Simulation

import random

# Define variables for Monte Carlo simulation
n_simulations = 1000
n_days = 365
starting_price = apple_data['Close'][-1]

# Calculate daily return mean and standard deviation
daily_return_mean = daily_returns.mean()
daily_return_std = daily_returns.std()

# Run Monte Carlo simulation
simulated_prices = []
for i in range(n_simulations):
    prices = [starting_price]
    for j in range(n_days):
        daily_return = random.gauss(daily_return_mean, daily_return_std)
        price = prices[-1] * (1 + daily_return)
        prices.append(price)
    simulated_prices.append(prices)

# Calculate mean and standard deviation of simulated prices
simulated_prices = np.array(simulated_prices)
mean_prices = simulated_prices.mean(axis=0)
std_prices = simulated_prices.std(axis=0)

# Plot simulated prices with confidence interval
plt.figure(figsize=(16,8))
plt.plot(mean_prices, label='Simulated Price')
plt.fill_between(range(n_days+1), mean_prices - 2*std_prices, mean_prices + 2*std_prices, alpha=0.2, label='95% CI')
plt.title("Apple Monte Carlo Simulation")
plt.xlabel("Days")
plt.ylabel("Stock Price ($)")
plt.legend()
plt.show()
