#data = pd.read_csv("data/raw/snb_FX.csv")

import pandas as pd
import requests
from io import StringIO
import os as os

start_date = '2000-01-01'
end_date = '2024-10-31'


urls = {
    "Norway": f'https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=off&txtcolor=%23444444&ts=12&tts=12&width=1320&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=IRSTCI01NOM156N&scale=left&cosd={start_date}&coed={end_date}&line_color=%234572a7&link_values=false&line_style=solid&mark_type=none&mw=3&lw=3&ost=-99999&oet=99999&mma=0&fml=a&fq=Monthly&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date={end_date}&revision_date={end_date}&nd={start_date}',
    "Japan": f'https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=off&txtcolor=%23444444&ts=12&tts=12&width=1320&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=IRSTCI01JPM156N&scale=left&cosd={start_date}&coed={end_date}&line_color=%234572a7&link_values=false&line_style=solid&mark_type=none&mw=3&lw=3&ost=-99999&oet=99999&mma=0&fml=a&fq=Monthly&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date={end_date}&revision_date={end_date}&nd={start_date}',
    "UK": f'https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=off&txtcolor=%23444444&ts=12&tts=12&width=1320&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=IRSTCI01GBM156N&scale=left&cosd={start_date}&coed={end_date}&line_color=%234572a7&link_values=false&line_style=solid&mark_type=none&mw=3&lw=3&ost=-99999&oet=99999&mma=0&fml=a&fq=Monthly&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date={end_date}&revision_date={end_date}&nd={start_date}',
    "United States": f'https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1320&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=IRSTCI01USM156N&scale=left&cosd={start_date}&coed={end_date}&line_color=%234572a7&link_values=false&line_style=solid&mark_type=none&mw=3&lw=3&ost=-99999&oet=99999&mma=0&fml=a&fq=Monthly&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date={end_date}&revision_date={end_date}&nd={start_date}',
    "Germany": f'https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=off&txtcolor=%23444444&ts=12&tts=12&width=1320&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=IRSTCI01DEM156N&scale=left&cosd={start_date}&coed={end_date}&line_color=%234572a7&link_values=false&line_style=solid&mark_type=none&mw=3&lw=3&ost=-99999&oet=99999&mma=0&fml=a&fq=Monthly&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date={end_date}&revision_date={end_date}&nd={start_date}',
    "Australia": f'https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=off&txtcolor=%23444444&ts=12&tts=12&width=1320&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=IRSTCI01AUM156N&scale=left&cosd={start_date}&coed={end_date}&line_color=%234572a7&link_values=false&line_style=solid&mark_type=none&mw=3&lw=3&ost=-99999&oet=99999&mma=0&fml=a&fq=Monthly&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date={end_date}&revision_date={end_date}&nd={start_date}',
    "New Zealand": f'https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=off&txtcolor=%23444444&ts=12&tts=12&width=1320&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=IRSTCI01NZM156N&scale=left&cosd={start_date}&coed={end_date}&line_color=%234572a7&link_values=false&line_style=solid&mark_type=none&mw=3&lw=3&ost=-99999&oet=99999&mma=0&fml=a&fq=Monthly&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date={end_date}&revision_date={end_date}&nd={start_date}',
    "Canada": f'https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=off&txtcolor=%23444444&ts=12&tts=12&width=1320&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=IRSTCI01CAM156N&scale=left&cosd={start_date}&coed={end_date}&line_color=%234572a7&link_values=false&line_style=solid&mark_type=none&mw=3&lw=3&ost=-99999&oet=99999&mma=0&fml=a&fq=Monthly&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date={end_date}&revision_date={end_date}&nd={start_date}'
}

###### FRED data ######
df_main = pd.DataFrame()

# Loop through the dictionary and download the data
for country, url in urls.items():
    response = requests.get(url)
    response.raise_for_status()  # Ensure we notice bad responses

    # Read the CSV data into a temporary DataFrame
    country_data = pd.read_csv(StringIO(response.text), delimiter=',')

    # Rename the last column to 'overnight_rate'
    country_data = country_data.rename(columns={country_data.columns[-1]: 'overnight_rate_pa',
                                                'DATE': 'date'})

    # Add a column to identify the country
    country_data['country'] = country

    # Append to the main DataFrame
    df_main = pd.concat([df_main, country_data], ignore_index=True)


###### SNB data ######
# Define file names
data_file = "devkua.csv"

# Download data
data_url = f"https://data.snb.ch/api/cube/zimoma/data/csv/en?fromDate={start_date[:7]}&toDate={end_date[:7]}"

# Fetch and save data
with requests.get(data_url) as r:
    with open(data_file, 'wb') as f:
        f.write(r.content)

# Load the data into a DataFrame
df_swi = pd.read_csv(data_file, skiprows=3, sep=";")
# delete temp file
if os.path.isfile(data_file):
    os.remove(data_file)

# data transformation
df_swi['Date'] = pd.to_datetime(df_swi['Date'], format='%Y-%m').dt.strftime('%Y-%m-%d')
df_swi.rename(columns={'Date': 'date', 'Value': 'overnight_rate_pa'}, inplace=True)

df_swi = df_swi[df_swi['D0'] == 'SARON'] #df_swi = df_swi[df_swi['D0'] == '1TGT']
df_swi['country'] = 'Switzerland'
df_swi = df_swi[['date', 'overnight_rate_pa', 'country']]


###### risksbank data ######
url = f'https://www.riksbank.se/en-gb/statistics/interest-rates-and-exchange-rates/search-interest-rates-and-exchange-rates/?a=M&c=Ultimo&from={start_date}&fs=3&s=g2-SECBREPOEFF&to={end_date}&d=Comma&export=csv'

# Fetch the content of the file
response = requests.get(url)
response.raise_for_status()  # Ensure we notice bad responses

# Load the Excel file directly into a pandas DataFrame
df_swe = pd.read_csv(StringIO(response.text), delimiter=';')

df_swe.rename(columns={df_swe.columns[0]: 'date'}, inplace=True)
df_swe.rename(columns={df_swe.columns[-1]: 'overnight_rate_pa'}, inplace=True)
df_swe['date'] = pd.to_datetime(df_swe['date'], format='%Y %B').dt.strftime('%Y-%m-%d')
df_swe['overnight_rate_pa'] = df_swe['overnight_rate_pa'].str.replace(',', '.', regex=False)
df_swe['overnight_rate_pa'] = pd.to_numeric(df_swe['overnight_rate_pa'], errors='coerce')
df_swe = df_swe[['date', 'overnight_rate_pa']]
df_swe['country'] = 'Sweden'


###### combine data ######
df = pd.concat([df_main, df_swi, df_swe], ignore_index=True)
print(df)
df.to_csv("data/raw/interest_rates.csv", index=False)