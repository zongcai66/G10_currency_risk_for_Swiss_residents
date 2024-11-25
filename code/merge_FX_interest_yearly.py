import pandas as pd
import numpy as np

# Load FX data
fx_url = "https://raw.githubusercontent.com/zongcai66/G10_currency_risk_for_Swiss_residents/refs/heads/main/data/transformed/yahoo_FX_2.csv"
rates_url = "https://raw.githubusercontent.com/zongcai66/G10_currency_risk_for_Swiss_residents/refs/heads/main/data/raw/interest_rates.csv"

# Load FX data
df_fx = pd.read_csv(fx_url, header=None, names=['date', 'ticker', 'type', 'value'])
df_fx = df_fx[df_fx['type'] == 'Adj Close']
df_fx['value'] = pd.to_numeric(df_fx['value'], errors='coerce')
df_fx = df_fx.dropna(subset=['value'])

# Convert date and identify month start
df_fx['date'] = pd.to_datetime(df_fx['date'])

# Calculate the first day of the month
df_fx['month_start'] = df_fx['date'].dt.to_period('M').dt.to_timestamp()

# Filter data for the first day of the month
df_fx = df_fx[df_fx['date'] == df_fx['month_start']]

# Calculate the date from the previous year
df_fx['prev_year_date'] = df_fx['date'] - pd.DateOffset(years=1)

# Merge to add previous year's values
df_fx = df_fx.merge(
    df_fx[['date', 'ticker', 'value']].rename(columns={'date': 'prev_year_date', 'value': 'prev_year_value'}),
    on=['ticker', 'prev_year_date'],
    how='left'
)

# Calculate log return
df_fx['log_return'] = np.log(df_fx['value'] / df_fx['prev_year_value'])

# Filter results: Keep only relevant columns (including log return)
df_fx = df_fx[['date', 'ticker', 'value', 'prev_year_value', 'log_return', 'month_start']]

# Map countries
df_fx['country'] = df_fx['ticker'].str[:3]
country_map = {
    'AUD': 'Australia', 'CAD': 'Canada', 'EUR': 'Germany', 'GBP': 'UK',
    'JPY': 'Japan', 'SEK': 'Sweden', 'USD': 'United States', 'NZD': 'New Zealand',
    'NOK': 'Norway', 'CHF': 'Switzerland'
}
df_fx['country'] = df_fx['country'].map(country_map)

# Load interest rates
df_rates = pd.read_csv(rates_url)
df_rates['date'] = pd.to_datetime(df_rates['date'])

# Check if column names in df_fx and df_rates match
print(f"Columns in df_fx: {df_fx.columns}")
print(f"Columns in df_rates: {df_rates.columns}")

# Ensure the columns for merging exist and are correctly named
df_rates = df_rates.rename(columns={'overnight_rate_pa': 'interest_rate', 'date': 'rate_date'})

# Merge FX data with interest rate data
df_merged = pd.merge(
    df_fx, 
    df_rates, 
    how='left', 
    left_on=['month_start', 'country'], 
    right_on=['rate_date', 'country']
)

# Find the Swiss interest rate for each date
df_switzerland = df_rates[df_rates['country'] == 'Switzerland'][['rate_date', 'interest_rate']]

# Merge the Swiss interest rate
df_merged = pd.merge(
    df_merged, 
    df_switzerland[['rate_date', 'interest_rate']], 
    how='left', 
    on='rate_date', 
    suffixes=('', '_switzerland')
)

# Calculate the logarithmic interest rate differential (percentages divided by 100): ln(1 + Swiss rate) - ln(1 + foreign rate)
df_merged['interest_rate_log_diff'] = np.log(1 + df_merged['interest_rate_switzerland'] / 100) - np.log(1 + df_merged['interest_rate'] / 100)

# Filter rows where log return is valid (remove NaN values if present)
df_merged = df_merged.dropna(subset=['log_return'])

# Check columns and output the first few rows
print("Columns in the merged DataFrame:")
print(df_merged.columns)
print("First rows of the merged and filtered data:")
print(df_merged.head())

# Save the final DataFrame
output_file = '../data/transformed/merged_FX_Interest_logreturns.csv'
df_merged.to_csv(output_file, index=False)
print(f"Merged data has been saved to '{output_file}'.")