# Import necessary libraries
import requests
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Set API endpoint and parameters
url = 'https://query1.finance.yahoo.com/v8/finance/chart/^GSPC'
params = {
    'range': 'max',
    'interval': '1d'
}

# Make API request
response = requests.get(url, params=params)
data = response.json()

# Clean data
df = pd.DataFrame(data['chart']['result'][0]['indicators']['quote'][0])
df['time'] = pd.to_datetime(data['chart']['result'][0]['timestamp'], unit='s')
df = df.set_index('time')
df = df.dropna()

# Calculate daily returns
df['returns'] = df['close'].pct_change()

# Compute moving averages
df['ma50'] = df['close'].rolling(window=50).mean()
df['ma200'] = df['close'].rolling(window=200).mean()

# Identify trends
plt.plot(df.index, df['close'], label='S&P 500')
plt.plot(df.index, df['ma50'], label='50-day MA')
plt.plot(df.index, df['ma200'], label='200-day MA')
plt.title('S&P 500 Index with Moving Averages')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.show()

# Perform simple linear regression
X = df[['returns']].dropna()
y = df['returns'].shift(-1).dropna()
model = LinearRegression()
model.fit(X, y)

# Make predictions
future_dates = pd.date_range(start=df.index[-1], periods=365, freq='D')
future_dates_df = pd.DataFrame(index=future_dates)
future_dates_df['predicted_returns'] = model.predict(future_dates_df.index.to_julian_date().values.reshape(-1, 1))

# Visualize predictions
plt.plot(df.index, df['returns'], label='Historical Returns')
plt.plot(future_dates_df.index, future_dates_df['predicted_returns'], label='Predicted Returns')
plt.title('S&P 500 Index Historical and Predicted Returns')
plt.xlabel('Date')
plt.ylabel('Returns')
plt.legend()
plt.show()
