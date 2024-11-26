import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#### parameters ####
alpha = 5

#### load data ####
df1_FX = pd.read_csv("data/raw/yahoo_FX.csv")
# Filter for 'Adj Close' type and drop rows with missing 'value'
df = df1_FX[df1_FX['type'] == 'Adj Close'].dropna(subset=['value'])
# Normalize the 'value' column by the first value for each ticker
df['normalized_value'] = df.groupby('ticker', group_keys=False)['value'].apply(lambda x: x / x.iloc[0])
df = df[~(df['normalized_value'] < 0.01)]

#### calculate basic statistics ####
df.loc[:, 'date'] = pd.to_datetime(df['date'])
# Sort the data by date and ticker (in case the data is not sorted)
df.sort_values(by=['ticker', 'date'], inplace=True)
# Calculate returns for each ticker
df.loc[:, 'return'] = df.groupby('ticker')['normalized_value'].pct_change()
# Drop the first row for each ticker since its return will be NaN
df = df.dropna(subset=['return'])
# Calculate statistics for each ticker
tickers = df['ticker'].unique()
stats = pd.DataFrame(columns=['std', 'VaR_5%', 'ES_5%'], index=tickers)
# Loop through each ticker to calculate the required metrics
for ticker in tickers:
    # Filter data for the current ticker
    ticker_data = df[df['ticker'] == ticker]
    # Calculate standard deviation (volatility)
    std = ticker_data['return'].std()
    # Calculate Value at Risk at 5% (5th percentile of the returns)
    VaR_5 = np.percentile(ticker_data['return'], alpha)
    # Calculate Expected Shortfall (ES) at 5% (average of returns below the 5th percentile)
    ES_5 = ticker_data[ticker_data['return'] <= VaR_5]['return'].mean()
    # Store the results in the stats DataFrame
    stats.loc[ticker] = [std, VaR_5, ES_5]


#### save plots ####
# Create a color palette for the unique tickers
tickers = stats.index
colors = sns.color_palette("husl", len(tickers))  # You can change the palette to suit your preference
ticker_colors = dict(zip(tickers, colors))  # Create a dictionary mapping tickers to colors

# 1. Plot for Standard Deviation of Returns (Volatility)
plt.figure(figsize=(12, 6))
plt.bar(stats.index, stats['std'], color=[ticker_colors[ticker] for ticker in stats.index], alpha=0.7)
plt.title("Standard Deviation of Returns for Each Currency Pair")
plt.xlabel("Currency Pair")
plt.ylabel("Standard Deviation (Volatility)")
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

# 2. Plot for Value at Risk (VaR) at 5% for each Currency Pair
plt.figure(figsize=(12, 6))
plt.bar(stats.index, stats['VaR_5%'], color=[ticker_colors[ticker] for ticker in stats.index], alpha=0.7)
plt.title("Value at Risk (VaR) at 5% for Each Currency Pair")
plt.xlabel("Currency Pair")
plt.ylabel("VaR at 5%")
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

# 3. Plot for Expected Shortfall (ES) at 5% for each Currency Pair
plt.figure(figsize=(12, 6))
plt.bar(stats.index, stats['ES_5%'], color=[ticker_colors[ticker] for ticker in stats.index], alpha=0.7)
plt.title("Expected Shortfall (ES) at 5% for Each Currency Pair")
plt.xlabel("Currency Pair")
plt.ylabel("ES at 5%")
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()