import pandas as pd

# Lade die CSV-Datei (ersetze 'your_file.csv' durch deinen Dateinamen)
df = pd.read_csv('yahoo_FX_2.csv')

# Funktion, um die '00' nach dem Dezimalpunkt zu entfernen
def clean_nok_value(value):
    if isinstance(value, float):
        str_value = str(value)
        if str_value.startswith('0.00'):
            return float('0.' + str_value[4:])
    return value

# Wende die Bereinigung auf die 'value'-Spalte an
df['value'] = df['value'].apply(clean_nok_value)

# Speichere die bereinigte Datei und überschreibe die ursprüngliche Datei
df.to_csv('yahoo_FX_2.csv', index=False)

print("Daten wurden bereinigt und die Datei wurde überschrieben.")