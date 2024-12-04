import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt

# URL of the CSV file containing modeling data
url = "https://raw.githubusercontent.com/zongcai66/G10_currency_risk_for_Swiss_residents/refs/heads/main/data/modeling_data/merged_FX_Interest_logreturns.csv"

# Load the CSV file from the URL
df = pd.read_csv(url)

# Countries included in the dataset
countries = df['country'].unique()

# List to store results (for the CSV file)
results_list = []

# Function to add stars for significance levels
def add_stars(p_value):
    if p_value < 0.01:
        return "***"
    elif p_value < 0.05:
        return "**"
    elif p_value < 0.1:
        return "*"
    return ""

# Function to format numerical values for display in the plot
def format_value(value):
    # If the value is numeric, format it to 2 decimal places
    if isinstance(value, (float, int)):
        return f"{value:.2f}"  # Formatierung auf 2 Dezimalstellen mit genauem Abstand
    return str(value)

# Function to format p-values with stars
def format_p_value(p_value):
    try:
        p_value_float = float(p_value)  # Try interpreting the p-value as a number
        stars = add_stars(p_value_float)  # Add stars if applicable
        return f"{stars} {p_value_float:.2f}"  # Stars on the left and aligned decimals
    except ValueError:
        return p_value  # Return the value as-is if it's already formatted

# Perform regression for each country
for country in countries:
    # Filter the data for each country
    country_data = df[df['country'] == country]
    
    # Set the y and x variables
    y = country_data['log_return']
    X = country_data['interest_rate_log_diff']
    
    # Add a constant term (intercept)
    X = sm.add_constant(X)
    
    # Perform the regression
    model = sm.OLS(y, X).fit()

    # Create a summary of the regression analysis
    summary = model.summary2()

    # Replace 'const' with 'alpha' and 'interest_rate_log_diff' with 'Beta'
    summary.tables[1].index = summary.tables[1].index.str.replace('const', 'alpha')
    summary.tables[1].index = summary.tables[1].index.str.replace('interest_rate_log_diff', 'Beta')

    # Format the table to 2 decimal places with alignment
    summary.tables[1] = summary.tables[1].applymap(lambda x: format_value(x))

    # Format p-values and add stars
    summary.tables[1]['P>|t|'] = summary.tables[1]['P>|t|'].apply(format_p_value)

    # Extract raw values for the CSV file (with 4 decimal places)
    alpha_row = model.params['const'], model.bse['const'], model.tvalues['const'], model.pvalues['const'], model.conf_int().loc['const', 0], model.conf_int().loc['const', 1]
    beta_row = model.params['interest_rate_log_diff'], model.bse['interest_rate_log_diff'], model.tvalues['interest_rate_log_diff'], model.pvalues['interest_rate_log_diff'], model.conf_int().loc['interest_rate_log_diff', 0], model.conf_int().loc['interest_rate_log_diff', 1]

    # Add values to the list for the CSV output (with 4 decimal places)
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

    # Create the plot with the summary as text
    fig, ax = plt.subplots(figsize=(12, 7))  # Create a plot with an appropriate size
    ax.axis('off')  # Disable axes
    
    # Format the summary for the plot (with 2 decimal places and alignment)
    formatted_text = summary.as_text()
    formatted_text = "\n".join([format_value(value) for value in formatted_text.split('\n')])

    # Print the summary text in the plot
    ax.text(0.1, 0.5, formatted_text, ha='left', va='center', fontsize=10, family='monospace')  # Monospace sorgt für die Ausrichtung der Dezimalstellen

    ax.set_title(f'Regression Summary for {country}', fontsize=12)

    # Save the plot as a PNG file
    output_dir = '../reports/figures'
    output_file = f'{output_dir}/regression_summary_{country}.png'
    plt.tight_layout()
    plt.savefig(output_file)

    # Close the plot
    plt.close()

    print(f"Regression summary for {country} saved to '{output_file}'")

# Convert the results into a DataFrame and save it as a CSV
results_df = pd.DataFrame(results_list)
output_csv = '../reports/figures/regression_summaries.csv'
results_df.to_csv(output_csv, index=False)
print(f"All regression results saved to '{output_csv}'")