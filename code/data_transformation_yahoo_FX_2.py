import pandas as pd
import os

# URL der Originaldatei
url = "https://raw.githubusercontent.com/zongcai66/G10_currency_risk_for_Swiss_residents/refs/heads/main/data/raw/yahoo_FX.csv"

# Lade die CSV-Datei von der URL
df = pd.read_csv(url)

# Funktion, um die '00' nach dem Dezimalpunkt nur bei NOKCHF zu entfernen
def clean_nok_value(row):
    if row['ticker'] == 'NOKCHF':  # Nur für NOKCHF-Daten
        value = row['value']
        if isinstance(value, float):
            str_value = str(value)
            if str_value.startswith('0.00'):
                row['value'] = float('0.' + str_value[4:])  # Nur ändern, wenn der Wert mit 0.00 beginnt
    return row

# Wende die Bereinigung auf die Zeilen an
df = df.apply(clean_nok_value, axis=1)

# Verzeichnis für den Ordner 'transformed' im übergeordneten Ordner erstellen, falls es noch nicht existiert
output_dir = '../data/transformed'  # Geht ein Verzeichnis nach oben und dann zum Ordner 'transformed'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Speichere die bereinigte Datei als 'yahoo_FX_2.csv' im Ordner 'data/transformed' im übergeordneten Verzeichnis
output_file = os.path.join(output_dir, 'yahoo_FX_2.csv')
df.to_csv(output_file, index=False)

print(f"Daten wurden bereinigt und als '{output_file}' gespeichert.")