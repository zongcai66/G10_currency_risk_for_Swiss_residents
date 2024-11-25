import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt

# URL der CSV-Datei mit den transformierten Daten
url = "https://raw.githubusercontent.com/zongcai66/G10_currency_risk_for_Swiss_residents/refs/heads/main/data/transformed/merged_FX_Interest_logreturns.csv"

# Lade die CSV-Datei von der URL
df = pd.read_csv(url)

# Länder, die im Datensatz enthalten sind
countries = df['country'].unique()

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

    # Formatiere alle numerischen Werte auf 4 Dezimalstellen
    summary.tables[1] = summary.tables[1].applymap(lambda x: f"{x:.4f}" if isinstance(x, (float, int)) else x)

    # Füge die Sterne für das Signifikanzniveau hinzu
    for idx in range(len(summary.tables[1])):
        p_value = float(summary.tables[1].iloc[idx]['P>|t|'])
        # Hinzufügen von Sternen basierend auf dem p-Wert
        if p_value < 0.01:
            summary.tables[1].iloc[idx, 3] = f"{summary.tables[1].iloc[idx, 3]} ***"
        elif p_value < 0.05:
            summary.tables[1].iloc[idx, 3] = f"{summary.tables[1].iloc[idx, 3]} **"
        elif p_value < 0.1:
            summary.tables[1].iloc[idx, 3] = f"{summary.tables[1].iloc[idx, 3]} *"

    # Erstelle das Plot mit der Zusammenfassung als Text
    fig, ax = plt.subplots(figsize=(10, 6))  # Erstelle ein Plot mit passender Größe
    ax.axis('off')  # Deaktiviere die Achsen
    ax.text(0.1, 0.5, summary.as_text(), ha='left', va='center', fontsize=10, family='monospace')  # Drucke die Zusammenfassung als Text im Plot
    ax.set_title(f'Regression Summary for {country}', fontsize=12)

    # Speichern des Plots als PNG-Datei
    output_dir = '../reports/figures'
    output_file = f'{output_dir}/regression_summary_{country}.png'
    plt.tight_layout()
    plt.savefig(output_file)

    # Schließen des Plots
    plt.close()

    print(f"Regression summary for {country} saved to '{output_file}'")