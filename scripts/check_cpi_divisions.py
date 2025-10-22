import pandas as pd

# Read the CPI data
cpi_df = pd.read_csv('cpi_2d_state.csv')

# Print unique divisions
print("Unique divisions in CPI data:")
print(cpi_df['division'].unique())

# Show a sample for each division
print("\nSample rows for each division:")
for div in cpi_df['division'].unique():
    print(f"\nDivision: {div}")
    print(cpi_df[cpi_df['division'] == div].head(2))