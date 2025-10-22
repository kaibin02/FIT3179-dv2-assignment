import pandas as pd

# --- Load dataset ---
df = pd.read_csv("income_cpi_analysis.csv")

# --- Basic checks ---
print("Columns available:", df.columns.tolist())

# --- Extract year from date ---
df["year"] = df["date"].astype(str).str[:4].astype(int)

# --- Ensure numeric type ---
df["income_median"] = pd.to_numeric(df["income_median"], errors="coerce")
df["index"] = pd.to_numeric(df["index"], errors="coerce")  # CPI index column

# --- Compute real median income (2010 prices) ---
df["income_median_real"] = df["income_median"] / (df["index"] / 100)

# --- Deduplicate by state-year ---
df_clean = (
    df.groupby(["state", "year"], as_index=False)
      .agg({"income_median_real": "mean"})
)

# --- Filter for 2022 only ---
df_2022 = df_clean[df_clean["year"] == 2022].copy()

# --- Sort and display ---
df_2022 = df_2022.sort_values("income_median_real", ascending=False)
print("\nReal Median Income by State (2022, in 2010 RM):")
print(df_2022.to_string(index=False, formatters={"income_median_real": "{:,.2f}".format}))

# --- Compute national mean of medians ---
national_mean = df_2022["income_median_real"].mean()
print(f"\nNational mean of medians (2022): RM {national_mean:,.2f}")

# --- Export cleaned version for Vega-Lite ---
df_2022.to_csv("income_2022_clean.csv", index=False)
print("\nSaved cleaned dataset as 'income_2022_clean.csv'")
