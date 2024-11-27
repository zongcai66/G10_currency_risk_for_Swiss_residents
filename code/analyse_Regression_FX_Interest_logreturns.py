import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt

# URL der CSV-Datei mit den transformierten Daten
url = "https://raw.githubusercontent.com/zongcai66/G10_currency_risk_for_Swiss_residents/refs/heads/main/data/transformed/merged_FX_Interest_logreturns.csv"

# Lade die CSV-Datei von der URL
df = pd.read_csv(url)

# Länder, die im Datensatz enthalten sind
countries = df['country'].unique()

# Liste für Ergebnisse (für die CSV-Datei)
results_list = []

# Funktion zum Hinzufügen von Sternchen für Signifikanz
def add_stars(p_value):
    if p_value < 0.01:
        return "***"
    elif p_value < 0.05:
        return "**"
    elif p_value < 0.1:
        return "*"
    return ""

# Funktion zur Formatierung von Zahlen für die Darstellung im Plot
def format_value(value):
    # Wenn der Wert numerisch ist, formatieren wir ihn auf 2 Dezimalstellen
    if isinstance(value, (float, int)):
        return f"{value:.2f}"  # Formatierung auf 2 Dezimalstellen mit genauem Abstand
    return str(value)

# Funktion zur Formatierung der P-Werte mit Sternchen
def format_p_value(p_value):
    try:
        p_value_float = float(p_value)  # Versuche den P-Wert als Zahl zu interpretieren
        stars = add_stars(p_value_float)  # Füge Sterne hinzu, falls erforderlich
        return f"{stars} {p_value_float:.2f}"  # Sterne links vom P-Wert und Dezimalstellen ausgerichtet
    except ValueError:
        return p_value  # Falls es sich um einen anderen Wert handelt (z. B. bereits formatiert)

# Führe die Regression für jedes Land durch
for country in countries:
    # Filtere die Daten für jedes Land
    country_data = df[df['country'] == country]
    
    # Setze die y- und x-Variablen
    y = country_data['log_return']
    X = country_data['interest_rate_log_diff']
    
    # Füge den konstanten Term (Intercept) hinzu
    X = sm.add_constant(X)
    
    # Führe die Regression durch
    model = sm.OLS(y, X).fit()

    # Erstelle eine Zusammenfassung der Regressionsanalyse
    summary = model.summary2()

    # Ersetze 'const' durch 'alpha' und 'interest_rate_log_diff' durch 'Beta'
    summary.tables[1].index = summary.tables[1].index.str.replace('const', 'alpha')
    summary.tables[1].index = summary.tables[1].index.str.replace('interest_rate_log_diff', 'Beta')

    # Formatierung der Tabelle auf 2 Dezimalstellen und Ausrichtung
    summary.tables[1] = summary.tables[1].applymap(lambda x: format_value(x))

    # P-Werte formatieren und Sterne hinzufügen
    summary.tables[1]['P>|t|'] = summary.tables[1]['P>|t|'].apply(format_p_value)

    # Extrahiere rohe Werte für die CSV-Datei (mit 4 Dezimalstellen)
    alpha_row = model.params['const'], model.bse['const'], model.tvalues['const'], model.pvalues['const'], model.conf_int().loc['const', 0], model.conf_int().loc['const', 1]
    beta_row = model.params['interest_rate_log_diff'], model.bse['interest_rate_log_diff'], model.tvalues['interest_rate_log_diff'], model.pvalues['interest_rate_log_diff'], model.conf_int().loc['interest_rate_log_diff', 0], model.conf_int().loc['interest_rate_log_diff', 1]

    # Füge die Werte zur Liste für die CSV-Ausgabe hinzu (mit 4 Dezimalstellen)
    results_list.append({
        'Country': country,
        'Alpha': f"{alpha_row[0]:.4f}",
        'Beta': f"{beta_row[0]:.4f}",
        'Alpha Std.Err.': f"{alpha_row[1]:.4f}",
        'Beta Std.Err.': f"{beta_row[1]:.4f}",
        'Alpha t': f"{alpha_row[2]:.4f}",
        'Beta t': f"{beta_row[2]:.4f}",
        'Alpha P>|t|': f"{alpha_row[3]:.4f}",
        'Beta P>|t|': f"{beta_row[3]:.4f}",
        'Alpha [0.025': f"{alpha_row[4]:.4f}",
        'Alpha 0.975]': f"{alpha_row[5]:.4f}",
        'Beta [0.025': f"{beta_row[4]:.4f}",
        'Beta 0.975]': f"{beta_row[5]:.4f}"
    })

    # Erstelle das Plot mit der Zusammenfassung als Text
    fig, ax = plt.subplots(figsize=(12, 7))  # Erstelle ein Plot mit passender Größe
    ax.axis('off')  # Deaktiviere die Achsen
    
    # Formatierung der Zusammenfassung für das Plot (mit 2 Dezimalstellen und Ausrichtung)
    formatted_text = summary.as_text()
    formatted_text = "\n".join([format_value(value) for value in formatted_text.split('\n')])

    # Drucke die Zusammenfassung als Text im Plot
    ax.text(0.1, 0.5, formatted_text, ha='left', va='center', fontsize=10, family='monospace')  # Monospace sorgt für die Ausrichtung der Dezimalstellen

    ax.set_title(f'Regression Summary for {country}', fontsize=12)

    # Speichern des Plots als PNG-Datei
    output_dir = '../reports/figures'
    output_file = f'{output_dir}/regression_summary_{country}.png'
    plt.tight_layout()
    plt.savefig(output_file)

    # Schließen des Plots
    plt.close()

    print(f"Regression summary for {country} saved to '{output_file}'")

# Konvertiere die Ergebnisse in einen DataFrame und speichere sie als CSV
results_df = pd.DataFrame(results_list)
output_csv = '../reports/figures/regression_summaries.csv'
results_df.to_csv(output_csv, index=False)
print(f"All regression results saved to '{output_csv}'")