import yfinance as yf
import pandas as pd


#Set the stock symbol and time period for the historical data
symbol = 'SPY'
start_date = '2010-01-01'
end_date = '2020-12-31'

#Use the yfinance library to get the historical data for the stock
data = yf.download(symbol, start_date, end_date)

#compute the relative strength index(RSI) using the closing prices and a 14-day window
rsi = data['Adj Close'].rolling(14).apply(lambda x: 100 - (100 / (1 + x.mean() / x.std())))

#create a new column in the data frame to store the RSI values 
data['RSI'] = rsi

# Get the trading calendar for the NYSE
nyse = yf.Calendar('NYSE')

#set the initial portfolio value and the initial number of shares
portfolio_value = 10000
num_shares = 0;

# Set the thresholds for the buy and sell signals
buy_threshold = 20
sell_threshold = 80

# Set the initial bet size
bet_size = 1000

# Iterate over the RSI values in the data
for i in range(len(data)):
    # Check if the current date is a trading day
    if nyse.is_trading_day(data.index[i]):
        # If the RSI value is below the buy threshold, buy shares
        if data['RSI'][i] < buy_threshold:
            # Calculate the number of shares to buy
            shares_to_buy = min(bet_size / data['Adj Close'][i], portfolio_value / data['Adj Close'][i])
            # Update the portfolio value and number of shares
            portfolio_value -= shares_to_buy * data['Adj Close'][i]
            num_shares += shares_to_buy
            # Double the bet size for the next round
            bet_size *= 2
        # If the RSI value is above the sell threshold, sell shares
        elif data['RSI'][i] > sell_threshold:
            # Update the portfolio value and number of shares
            portfolio_value += num_shares * data['Adj Close'][i]
            num_shares = 0
            # Reset the bet size
            bet_size = 1000

# Print the final portfolio value and number of shares
print(f"Portfolio value: {portfolio_value:.2f}")
print(f"Number of shares: {num_shares:.0f}")
