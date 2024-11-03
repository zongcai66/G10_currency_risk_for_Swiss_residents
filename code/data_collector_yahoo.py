import requests
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

tickers = {
    "SHY": "US (USD)",
    "XSB.TO": "Canada (CAD)",
    "IGLS.L": "UK (GBP)",
    #"XACT-SVERIGE.ST": "Sweden (SEK)",
    "CSBGC3.SW": "Switzerland (CHF)",
    "IBGS.MI": "Eurozone (EUR)",
    "XJSE.DE": "Japan (EUR)"
}


start_date = "2004-01-01"
end_date = "2024-10-21"

# Download the data
df = yf.download(list(tickers.keys()), start=start_date, end=end_date, progress=False)

# Convert the data to long format
df_long = df.stack(['Ticker', 'Price'], future_stack=True).reset_index()
df_long.rename(columns={'Date': 'date', 'Ticker': 'ticker', 'Price': 'type', 0: 'value'}, inplace=True)
df_long['date'] = df_long['date'].dt.date
df_long['ticker'] = df_long['ticker'].map(tickers)

df_long = df_long.dropna(subset=['value'])
df_long.to_csv("data/raw/yahoo_FX.csv", index=False)

print(df_long)