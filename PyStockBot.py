
import yfinance as yf
import pandas as pd

symbol = 'SPY'
start_date = '2010-01-01'
end_date = '2020-12-31'

stock = yf.Ticker(symbol)
data = stock.history(start=start_date, end=end_date)

# Shift the closing prices by one day
data['prev_close'] = data['Close'].shift(1)

# Calculate the difference between the current and previous closing prices
data['diff'] = data['Close'] - data['prev_close']


# Calculate the average gain and the average loss for the stock
avg_gain = data.loc[data['diff'] > 0, 'diff'].mean()
avg_loss = data.loc[data['diff'] < 0, 'diff'].mean()

# Calculate the relative strength and the relative strength ratio
rs = avg_gain / abs(avg_loss)
rsr = avg_gain / (avg_gain + abs(avg_loss))

RSI = 100 - (100 / (1 + RSR))
