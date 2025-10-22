import pandas as pd
import os
from pathlib import Path

# Get the script's directory and set working directory
script_dir = Path(__file__).parent.parent
os.chdir(script_dir)

try:
    # Load the data
    print("Loading income_cpi_analysis.csv...")
    df = pd.read_csv("income_cpi_analysis.csv")
    
    # Basic info about the data
    print("\nData shape (rows, columns):", df.shape)
    print("\nColumns in the data:", df.columns.tolist())
    
    # Show how many rows we have for each state
    print("\nRows per state:")
    state_counts = df['state'].value_counts()
    print(state_counts)
    
    # Extract year from date for filtering
    df['year'] = df['date'].astype(str).str[:4].astype(int)
    
    # Filter for 2022 data
    df_2022 = df[df['year'] == 2022].copy()
    print("\n2022 Data - State and Income Values:")
    print("=" * 60)
    result = df_2022[['state', 'income_median', 'cpi_index_annual', 'income_median_real']].sort_values('state')
    result = result.rename(columns={
        'income_median': 'Nominal Income',
        'cpi_index_annual': 'CPI Index',
        'income_median_real': 'Real Income'
    })
    pd.set_option('display.float_format', lambda x: '{:,.2f}'.format(x))
    print(result.to_string(index=False))

except Exception as e:
    print(f"\nError occurred: {str(e)}")