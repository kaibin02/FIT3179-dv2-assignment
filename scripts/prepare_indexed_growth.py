import pandas as pd

# Read the original data
df = pd.read_csv('../income_2012-2022.csv')

# Extract year from date
df['year'] = df['date'].astype(str).str[:4].astype(int)

# Calculate CPI adjustment factor (2012 as base year)
cpi_2012 = df[df['year'] == 2012]['cpi'].iloc[0]
df['cpi_factor'] = cpi_2012 / df['cpi']

# Calculate real income values
df['income_median_real'] = df['income_median'] * df['cpi_factor']

# Save the processed data
df.to_csv('../income_cpi_analysis.csv', index=False)