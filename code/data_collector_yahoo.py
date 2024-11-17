import yfinance as yf
import pandas as pd

g10_chf_tickers = [
    "EURCHF=X",  # Euro
    "GBPCHF=X",  # British Pound
    "USDCHF=X",  # US Dollar
    "CADCHF=X",  # Canadian Dollar
    "SEKCHF=X",  # Swedish Krona
    "JPYCHF=X",   # Japanese Yen
    "AUDCHF=X",  # Australian Dollar
    "NZDCHF=X",  # New Zealand Dollar
    "NOKCHF=X"   # Norwegian Krone
]

# Define the date range for the data
start_date = "2004-01-01"
end_date = "2024-10-21"

# Download the data
df = yf.download(g10_chf_tickers, start=start_date, end=end_date, progress=False)

df_long = df.stack(['Ticker', 'Price'], future_stack=True).reset_index()
df_long.rename(columns={'Date': 'date', 'Ticker': 'ticker', 'Price': 'type', 0: 'value'}, inplace=True)
df_long['date'] = df_long['date'].dt.strftime('%Y-%m-%d')
df_long['ticker'] = df_long['ticker'].str.replace('=X', '')
df_long = df_long.dropna(subset=['value'])
df_long.to_csv("data/raw/yahoo_FX.csv", index=False)

print(df_long)