import requests
import os
import pandas as pd

# Define file names
data_file = "devkua.csv"

# Download data
data_url = "https://data.snb.ch/api/cube/zimoma/data/csv/en?fromDate=2000-01&toDate=2024-09"

# Fetch and save data
with requests.get(data_url) as r:
    with open(data_file, 'wb') as f:
        f.write(r.content)

# Load the data into a DataFrame
data = pd.read_csv(data_file, skiprows=3, sep=";")
data['Date'] = pd.to_datetime(data['Date'], format='%Y-%m')
data.to_csv("data/raw/snb_FX.csv", index=False)
print(data)

# delete temp file
if os.path.isfile(data_file):
    os.remove(data_file)