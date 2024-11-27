import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import random

# Define the relative path to the 'figures' folder within the 'reports' folder (at the same level as the 'code' folder)
figures_dir = os.path.join(os.path.dirname(os.getcwd()), 'reports', 'figures')

# Ensure the 'figures' folder exists
if not os.path.exists(figures_dir):
    os.makedirs(figures_dir)

# Load the CSV data from the remote repository
df = pd.read_csv("https://raw.githubusercontent.com/zongcai66/G10_currency_risk_for_Swiss_residents/refs/heads/main/data/transformed/yahoo_FX_2.csv", header=None, names=['Date', 'Currency Pair', 'Type', 'Value'])

# Filter only the rows with the type 'Adj Close'
df_adj_close = df[df['Type'] == 'Adj Close'].copy()

# Convert the 'Date' column to datetime format
df_adj_close['Date'] = pd.to_datetime(df_adj_close['Date'])

# Ensure that the 'Value' column contains only numeric values
df_adj_close['Value'] = pd.to_numeric(df_adj_close['Value'], errors='coerce')

# Drop rows with NaN values
df_adj_close.dropna(subset=['Value'], inplace=True)

# Pivot the data so that currency pairs are columns and dates are the index
df_pivot = df_adj_close.pivot(index='Date', columns='Currency Pair', values='Value')

# Calculate the daily returns for each currency pair
df_returns = df_pivot.pct_change().dropna()

# Calculate the Value-at-Risk (VaR) as the 5% percentile of the daily returns
var_95 = df_returns.quantile(0.05, axis=0)

# Set the Seaborn style for the plots
sns.set(style="whitegrid")

# Calculate the number of currency pairs
n_assets = len(df_returns.columns)

# Calculate the required number of rows and columns for the subplots
n_rows = (n_assets + 1) // 2  # Calculate the number of rows
n_cols = 2  # 2 columns

# Create subplots for the returns and VaR diagrams with a larger plot size
fig, axes = plt.subplots(nrows=n_rows, ncols=n_cols, figsize=(15, 5 * n_rows))

# Flatten the axes for easier iteration
axes = axes.flatten()

# Create histograms for the daily returns and plot the VaR
for i, column in enumerate(df_returns.columns):
    axes[i].hist(df_returns[column].dropna(), bins=50, alpha=0.7, color='blue', label=f"Returns {column}")
    axes[i].axvline(var_95[column], color='red', linestyle='dashed', linewidth=2, label=f"VaR 5%: {var_95[column]:.4f}")
    axes[i].set_title(f"Returns and VaR for {column}", fontsize=14)
    axes[i].set_xlabel('Return', fontsize=12)
    axes[i].set_ylabel('Frequency', fontsize=12)
    axes[i].legend(fontsize=10)

# Prevent overlapping of the plots
plt.tight_layout()

# Save the VaR plot as a PNG file in the 'figures' folder
plt.savefig(os.path.join(figures_dir, 'returns_var_plot.png'), dpi=300)  # Save with higher resolution
plt.show()  # Show the VaR plot

# Calculate the average daily return and the standard deviation of returns for each currency pair
mean_returns = df_returns.mean()
std_returns = df_returns.std()

# Save the plot for the average daily return
plt.figure(figsize=(12, 6))
plt.bar(mean_returns.index, mean_returns.values, color='green', alpha=0.7)
plt.title("Average Daily Return for Each Currency Pair")
plt.xlabel("Currency Pair")
plt.ylabel("Average Daily Return")
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig(os.path.join(figures_dir, 'average_return_plot.png'), dpi=300)  # Save in the 'figures' folder
plt.show()

# Save the plot for the standard deviation of returns
plt.figure(figsize=(12, 6))
plt.bar(std_returns.index, std_returns.values, color='orange', alpha=0.7)
plt.title("Standard Deviation of Daily Returns for Each Currency Pair")
plt.xlabel("Currency Pair")
plt.ylabel("Standard Deviation of Return")
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig(os.path.join(figures_dir, 'std_deviation_return_plot.png'), dpi=300)  # Save in the 'figures' folder
plt.show()

# Create a line plot for the currency exchange rates
plt.figure(figsize=(12, 6))
for column in df_pivot.columns:
    plt.plot(df_pivot.index, df_pivot[column], label=column)

plt.title("Currency Exchange Rates Over Time")
plt.xlabel("Date")
plt.ylabel("Adj Close Value")
plt.legend()

# Save the currency exchange rate plot as a PNG file in the 'figures' folder
plt.savefig(os.path.join(figures_dir, 'exchange_rate_plot.png'), dpi=300)  # Save in the 'figures' folder
plt.show()  # Show the currency exchange rate plot

# Monte Carlo Simulation for CHF against each currency
num_simulations = 10
num_days = 252
last_price = df_pivot.iloc[-1, :]  # Last prices for each currency pair
last_ret = df_returns.iloc[-1, :]  # Last returns for each currency pair
daily_vol = df_returns.std()  # Daily volatility for each currency pair

# Define the function to calculate VaR using the Monte Carlo simulation
def mcVaR(simulation_df_ret, alpha=5):
    return np.percentile(simulation_df_ret, alpha)

# Loop through each currency pair (excluding CHF)
for i, column in enumerate(df_returns.columns):
    if column != 'CHF':  # Skip CHF as we compare each currency to CHF
        simulation_df_rate = pd.DataFrame()
        simulation_df_ret = pd.DataFrame()

        # Perform simulations
        for x in range(num_simulations):
            count = 0
            daily_voli = daily_vol[column]

            # Generate simulated price series
            price_series = []
            price = last_price[column] * (1 + np.random.normal(0, daily_vol[column]))
            price_series.append(price)

            # Generate simulated return series
            ret_series = []
            ret = random.normalvariate(last_ret[column], daily_vol[column])
            ret_series.append(ret)

            # Generate the price and return paths for the given number of days
            for y in range(num_days):
                price = price_series[count] * (1 + np.random.normal(0, daily_vol[column]))
                price_series.append(price)
                ret = random.normalvariate(last_ret[column], daily_vol[column])
                ret_series.append(ret)
                count += 1

            simulation_df_rate[x] = price_series
            simulation_df_ret[x] = ret_series

        # Plot and save the Price Simulation for this currency pair (against CHF)
        plt.figure(figsize=(10, 6))
        plt.plot(simulation_df_rate)
        plt.suptitle(f'Monte Carlo Price Simulation for {column} (vs CHF)')
        plt.axhline(y=last_price[column], color='r', linestyle='-', label='Last Price')
        plt.xlabel('Days')
        plt.ylabel('Price')
        plt.legend()
        plt.tight_layout()

        # Save the simulation plot
        price_simulation_filename = f'monte_carlo_price_simulation_{column}_vs_CHF.png'
        plt.savefig(os.path.join(figures_dir, price_simulation_filename), dpi=300)  # Save the figure
        plt.close()  # Close the plot to avoid overlap with other plots

        # Calculate the VaR using the simulated returns and add it to the VaR list
        portResults = pd.Series(simulation_df_ret.iloc[-1, :])
        VaR_3 = mcVaR(portResults, alpha=5)

        print(f"VaR for {column} against CHF: {VaR_3:.4f}")

        # Monte Carlo VaR Plot (instead of Price)
        plt.figure(figsize=(10, 6))
        plt.plot(simulation_df_ret)
        plt.axhline(y=var_95[column], color='r', linestyle='dashed', label=f'VaR 5%: {var_95[column]:.4f}')
        plt.title(f'Monte Carlo VaR Simulation for {column} (vs CHF)')
        plt.xlabel('Days')
        plt.ylabel('Simulated Returns')
        plt.legend()
        plt.tight_layout()

        # Save the VaR simulation plot
        var_simulation_filename = f'monte_carlo_var_simulation_{column}_vs_CHF.png'
        plt.savefig(os.path.join(figures_dir, var_simulation_filename), dpi=300)  # Save the figure
        plt.close()  # Close the plot to avoid overlap with other plots

# Create a separate plot to compare VaR 5% values across all currencies
plt.figure(figsize=(12, 6))
plt.bar(var_95.index, var_95.values, color='purple', alpha=0.7)
plt.title("VaR 5% Comparison for All Currency Pairs (vs CHF)")
plt.xlabel("Currency Pair")
plt.ylabel("VaR 5% Value")
plt.xticks(rotation=90)
plt.tight_layout()

# Save the comparison plot for VaR 5% values
plt.savefig(os.path.join(figures_dir, 'var_5_percent_comparison_plot.png'), dpi=300)  # Save in the 'figures' folder
plt.show()  # Show the VaR 5% comparison plot

# Store the historical VaR and Monte Carlo VaR in a table
monte_carlo_vars = {}

for column in df_returns.columns:
    simulation_df_ret = pd.DataFrame()

    for _ in range(num_simulations):
        simulated_returns = np.random.normal(loc=0, scale=daily_vol[column], size=num_days)
        simulation_df_ret = pd.concat(
            [simulation_df_ret, pd.Series(simulated_returns)], axis=1)

    # Monte Carlo VaR
    mc_var = np.percentile(simulation_df_ret.iloc[-1, :], 5)
    monte_carlo_vars[column] = mc_var

# create table
result_df = pd.DataFrame({
    'Currency Pair': var_95.index,
    'Historical VaR (5%)': var_95.values,
    'Monte Carlo VaR (5%)': [monte_carlo_vars[currency] for currency in
                             var_95.index]
})

output_path = os.path.join(figures_dir, 'VaR_results.csv')
result_df.to_csv(output_path, index=False)
