import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

#### parameters ####
alpha = 5  # Value-at-Risk level (in percentile)
freq = 'M'  # Frequency for resampling ('D' = daily, 'M' = monthly, 'Q' = quarterly, '2A' = semi-annually, 'A' = annually)

#### load data ####
df1_FX = pd.read_csv("../data/raw/yahoo_FX.csv")
# Filter for 'Adj Close' type and drop rows with missing 'value'
df = df1_FX[df1_FX['type'] == 'Adj Close'].dropna(subset=['value'])
# Normalize the 'value' column by the first value for each ticker
df['normalized_value'] = df.groupby('ticker', group_keys=False)['value'].apply(lambda x: x / x.iloc[0])
df = df[~(df['normalized_value'] < 0.01)]

#### calculate basic statistics ####
df.loc[:, 'date'] = pd.to_datetime(df['date'])  # Ensure 'date' is in datetime format
df = df.sort_values(by=['ticker', 'date'])

# Function to calculate returns at different frequencies
def calculate_returns(df, freq='D'):
    """
    Calculate returns at different frequencies.
    freq: Frequency for resampling ('D' = daily, 'M' = monthly, 'Q' = quarterly, '2A' = semi-annually, 'A' = annually)
    """
    df = df.set_index('date')  # Ensure 'date' is the index for resampling
    return df.groupby('ticker')['normalized_value'].resample(freq).last().pct_change().dropna()

# Calculate returns for the selected frequency
df_returns = calculate_returns(df, freq=freq)

# Calculate statistics for each ticker
tickers = df_returns.index.get_level_values('ticker').unique()
stats = pd.DataFrame(columns=['std', 'VaR', 'ES'], index=tickers)
# Loop through each ticker to calculate the required metrics
for ticker in tickers:
    # Filter data for the current ticker
    ticker_data = df_returns[df_returns.index.get_level_values('ticker') == ticker]
    # Calculate standard deviation (volatility)
    std = ticker_data.std()
    # Calculate Value at Risk at 5% (5th percentile of the returns)
    VaR_5 = np.percentile(ticker_data, alpha)
    # Calculate Expected Shortfall (ES) at 5% (average of returns below the 5th percentile)
    ES_5 = ticker_data[ticker_data <= VaR_5].mean()
    # Store the results in the stats DataFrame
    stats.loc[ticker] = [std, VaR_5, ES_5]

#### save plots and results ####
# Create a color palette for the unique tickers
tickers = stats.index
colors = sns.color_palette("husl", len(tickers))  # You can change the palette to suit your preference
ticker_colors = dict(zip(tickers, colors))  # Create a dictionary mapping tickers to colors

# Plot titles dynamically adjusted with the alpha value and frequency
alpha_title = f"({alpha}% Confidence Level)"
freq_map = {
    'D': 'Daily',
    'M': 'Monthly',
    'Q': 'Quarterly',
    '2A': 'Semi-Annually',
    'A': 'Annually'
}
freq_title = freq_map.get(freq, 'Unknown Frequency')

# Create the "reports/figures" directory if it doesn't exist
# os.makedirs("reports/figures", exist_ok=True)

# 1. Plot for Standard Deviation of Returns (Volatility)
plt.figure(figsize=(12, 6))
plt.bar(stats.index, stats['std'], color=[ticker_colors[ticker] for ticker in stats.index], alpha=0.7)
plt.title(f"Standard Deviation of Returns for Each Currency Pair ({freq_title}) {alpha_title}")
plt.xlabel("Currency Pair")
plt.ylabel(f"Standard Deviation (Volatility) - {alpha_title}")
plt.xticks(rotation=90)
plt.tight_layout()
# Save the plot as a PNG file
plt.savefig("../reports/figures/volatility_plot.png")
plt.close()

# 2. Plot for Value at Risk (VaR) at 5% for each Currency Pair
plt.figure(figsize=(12, 6))
plt.bar(stats.index, stats['VaR'], color=[ticker_colors[ticker] for ticker in stats.index], alpha=0.7)
plt.title(f"Value at Risk (VaR) at 5% for Each Currency Pair ({freq_title}) {alpha_title}")
plt.xlabel("Currency Pair")
plt.ylabel(f"VaR at 5% {alpha_title}")
plt.xticks(rotation=90)
plt.tight_layout()
# Save the plot as a PNG file
plt.savefig("../reports/figures/VaR_5_percent_plot.png")
plt.close()

# 3. Plot for Expected Shortfall (ES) at 5% for each Currency Pair
plt.figure(figsize=(12, 6))
plt.bar(stats.index, stats['ES'], color=[ticker_colors[ticker] for ticker in stats.index], alpha=0.7)
plt.title(f"Expected Shortfall (ES) at 5% for Each Currency Pair ({freq_title}) {alpha_title}")
plt.xlabel("Currency Pair")
plt.ylabel(f"ES at 5% {alpha_title}")
plt.xticks(rotation=90)
plt.tight_layout()
# Save the plot as a PNG file
plt.savefig("../reports/figures/ES_5_percent_plot.png")
plt.close()

# Save the statistics DataFrame as a CSV file
stats.to_csv("../reports/figures/statistics_results.csv")
