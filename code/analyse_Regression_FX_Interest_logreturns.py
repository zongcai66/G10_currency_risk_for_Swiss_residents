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

    # Formatiere alle numerischen Werte auf 4 Dezimalstellen für die PNG-Ausgabe
    summary.tables[1] = summary.tables[1].applymap(lambda x: f"{x:.4f}" if isinstance(x, (float, int)) else x)

    # Extrahiere rohe Werte für die CSV-Datei vor dem Hinzufügen von Sternchen
    alpha_row = model.params['const'], model.bse['const'], model.tvalues['const'], model.pvalues['const'], model.conf_int().loc['const', 0], model.conf_int().loc['const', 1]
    beta_row = model.params['interest_rate_log_diff'], model.bse['interest_rate_log_diff'], model.tvalues['interest_rate_log_diff'], model.pvalues['interest_rate_log_diff'], model.conf_int().loc['interest_rate_log_diff', 0], model.conf_int().loc['interest_rate_log_diff', 1]

    # Füge die Werte zur Liste hinzu
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

    # Füge die Sterne für das Signifikanzniveau hinzu (nur für die PNG-Ausgabe)
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

# Konvertiere die Ergebnisse in einen DataFrame und speichere sie als CSV
results_df = pd.DataFrame(results_list)
output_csv = '../reports/figures/regression_summaries.csv'
results_df.to_csv(output_csv, index=False)
print(f"All regression results saved to '{output_csv}'")