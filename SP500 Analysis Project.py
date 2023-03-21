import requests
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Set API endpoint and parameters
api_key = 'G5VBBZPVHKYBKOX6'  
symbol = 'SPX'
function = 'TIME_SERIES_DAILY_ADJUSTED'
params = {
    'function': function,
    'symbol': symbol,
    'outputsize': 'full',
    'apikey': api_key
}

# Make API request
url = 'https://www.alphavantage.co/query'
response = requests.get(url, params=params)
data = response.json()

# Clean data
df = pd.DataFrame(data['Time Series (Daily)']).T
df.index = pd.to_datetime(df.index)
df = df[['1. open', '2. high', '3. low', '4. close']]
df = df.astype('float')
df.columns = ['open', 'high', 'low', 'close']
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
