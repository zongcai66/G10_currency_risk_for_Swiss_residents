import requests
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


#test 3
# Define file names
data_file = "devkua.csv"
structure_file = "devkua.json"

# Download data
data_url = "https://data.snb.ch/api/cube/zimoma/data/csv/en?fromDate=2000-01&toDate=2024-09"
structure_url = "https://data.snb.ch/api/cube/devkua/dimensions/en"

# Fetch and save data
with requests.get(data_url) as r:
    with open(data_file, 'wb') as f:
        f.write(r.content)

with requests.get(structure_url) as r:
    with open(structure_file, 'wb') as f:
        f.write(r.content)

# Load the data into a DataFrame
data = pd.read_csv(data_file, skiprows=3, sep=";")
data['Date'] = pd.to_datetime(data['Date'], format='%Y-%m')

data
