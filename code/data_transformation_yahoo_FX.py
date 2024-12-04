import pandas as pd
import os

# URL of the original file
url = "https://raw.githubusercontent.com/zongcai66/G10_currency_risk_for_Swiss_residents/refs/heads/main/data/raw/yahoo_FX.csv"

# Load the CSV file from the URL
df = pd.read_csv(url)

# Function to remove the '00' after the decimal point only for NOKCHF
def clean_nok_value(row):
    if row['ticker'] == 'NOKCHF':  # Only for NOKCHF data
        value = row['value']
        if isinstance(value, float):
            str_value = str(value)
            if str_value.startswith('0.00'):
                row['value'] = float('0.' + str_value[4:])  # Change only if the value starts with 0.00
    return row

# Apply the cleaning function to the rows
df = df.apply(clean_nok_value, axis=1)

# Create a directory for the 'modeling_data' folder in the parent directory if it doesn't already exist
output_dir = '../data/modeling_data'  # Go one directory up and then to the 'modeling_data' folder
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Save the cleaned file as 'yahoo_FX_2.csv' in the 'data/modeling_data' folder in the parent directory
output_file = os.path.join(output_dir, 'yahoo_FX_2.csv')
df.to_csv(output_file, index=False)

print(f"Data has been cleaned and saved as '{output_file}'.")