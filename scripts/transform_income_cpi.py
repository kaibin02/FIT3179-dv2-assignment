import pandas as pd
import numpy as np

# Read the data
cpi_df = pd.read_csv('cpi_2d_state.csv')
income_df = pd.read_csv('hh_income_state.csv')

# Convert dates to datetime
cpi_df['date'] = pd.to_datetime(cpi_df['date'])
income_df['date'] = pd.to_datetime(income_df['date'])

# Add year columns
cpi_df['year'] = cpi_df['date'].dt.year
income_df['year'] = income_df['date'].dt.year

# Filter CPI data for overall division and calculate annual mean
cpi_annual = (cpi_df[cpi_df['division'] == 'overall']
              .groupby(['state', 'year'])['index']
              .mean()
              .reset_index()
              .rename(columns={'index': 'cpi_index_annual'}))

# Merge income and CPI data
merged_df = pd.merge(
    income_df,
    cpi_annual,
    on=['state', 'year'],
    how='inner'
)

# Calculate derived metrics
def calculate_yoy_pct(group, value_col):
    group = group.sort_values('year')
    group[f'{value_col}_yoy'] = group[value_col].pct_change() * 100
    return group

# Real income calculations
merged_df['income_median_real'] = merged_df['income_median'] / (merged_df['cpi_index_annual']/100)
merged_df['income_mean_real'] = merged_df['income_mean'] / (merged_df['cpi_index_annual']/100)

# YoY changes
merged_df = merged_df.groupby('state').apply(
    lambda x: calculate_yoy_pct(x, 'cpi_index_annual')
).reset_index(drop=True)
merged_df = merged_df.rename(columns={'cpi_index_annual_yoy': 'inflation_yoy_pct'})

merged_df = merged_df.groupby('state').apply(
    lambda x: calculate_yoy_pct(x, 'income_median_real')
).reset_index(drop=True)
merged_df = merged_df.rename(columns={'income_median_real_yoy': 'median_real_yoy_pct'})

# Mean-median gap
merged_df['mean_median_gap_pct'] = (merged_df['income_mean'] / merged_df['income_median'] - 1) * 100

# Indexed values (base year = first year for each state)
for metric in ['income_median', 'income_median_real', 'income_mean', 'income_mean_real', 'cpi_index_annual']:
    merged_df[f'{metric}_indexed'] = merged_df.groupby('state').apply(
        lambda x: (x[metric] / x[metric].iloc[0]) * 100
    ).reset_index(drop=True)

# Rankings
def add_rankings(df, year):
    year_data = df[df['year'] == year].copy()
    year_data['rank_median_nominal'] = year_data['income_median'].rank(ascending=False)
    year_data['rank_median_real'] = year_data['income_median_real'].rank(ascending=False)
    return year_data[['state', 'rank_median_nominal', 'rank_median_real']]

# Add rankings for each year
all_rankings = []
for year in merged_df['year'].unique():
    all_rankings.append(add_rankings(merged_df, year))

rankings_df = pd.concat(all_rankings)
merged_df = pd.merge(merged_df, rankings_df, on='state', how='left')

# Select and order columns
columns_order = [
    'state', 'date', 'year',
    'income_median', 'income_mean', 
    'cpi_index_annual', 'inflation_yoy_pct',
    'income_median_real', 'income_mean_real',
    'median_real_yoy_pct', 'mean_median_gap_pct',
    'income_median_indexed', 'income_mean_indexed',
    'income_median_real_indexed', 'income_mean_real_indexed',
    'cpi_index_annual_indexed',
    'rank_median_nominal', 'rank_median_real'
]

final_df = merged_df[columns_order].sort_values(['state', 'year'])

# Save to CSV
final_df.to_csv('income_cpi_analysis.csv', index=False)

# Print sample of final dataset
print("\nFirst few rows of the transformed dataset:")
print(final_df.head())

print("\nColumns in the final dataset:")
print(final_df.columns.tolist())

print("\nSummary statistics:")
print(final_df.describe())