import pandas as pd

# Read the data
df = pd.read_csv('income_cpi_analysis.csv')

# Print some statistics before deduplication
print(f"Original number of rows: {len(df)}")
print("\nDuplicate counts by state and year:")
print(df[df.duplicated(keep=False)].groupby(['state', 'year']).size().reset_index(name='count').sort_values('count', ascending=False).head())

# Remove duplicates while keeping the first occurrence
df_deduped = df.drop_duplicates()

# Print statistics after deduplication
print(f"\nRows after deduplication: {len(df_deduped)}")
print(f"Removed {len(df) - len(df_deduped)} duplicate rows")

# Save the deduplicated data
df_deduped.to_csv('income_cpi_analysis_deduped.csv', index=False)
print("\nDeduplicated data saved to 'income_cpi_analysis_deduped.csv'")