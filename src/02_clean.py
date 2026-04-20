"""
02_clean.py
-----------
Stage 3: Data Cleaning and Merging
BEE2041 Empirical Project — Green Copper

What this script does:
  1. Loads raw copper price data (FRED, monthly) and renewable capacity data (IRENA, annual)
  2. Parses dates and extracts year from the copper series
  3. Aggregates monthly copper prices to annual means
  4. Standardises column names
  5. Merges the two datasets on year
  6. Saves one clean CSV to data/clean/merged_clean.csv

Inputs:
  data/raw/copper_prices.csv      — FRED copper price series (DATE, VALUE)
  data/raw/renewable_capacity.csv — IRENA renewable capacity series (Year, Value)

Output:
  data/clean/merged_clean.csv
"""

import pandas as pd
import os

# ---------------------------------------------------------------------------
# 0. Paths — all relative so the script works on any machine after cloning
# ---------------------------------------------------------------------------

RAW_DIR   = os.path.join("data", "raw")
CLEAN_DIR = os.path.join("data", "clean")

COPPER_FILE    = os.path.join(RAW_DIR, "copper_prices.csv")
RENEWABLE_FILE = os.path.join(RAW_DIR, "renewable_capacity.csv")
OUTPUT_FILE    = os.path.join(CLEAN_DIR, "merged_clean.csv")

# Create the clean directory if it does not already exist
os.makedirs(CLEAN_DIR, exist_ok=True)


# ---------------------------------------------------------------------------
# 1. Load raw data
# ---------------------------------------------------------------------------

print("Loading raw data...")

copper_raw    = pd.read_csv(COPPER_FILE)
renewable_raw = pd.read_csv(RENEWABLE_FILE)

print(f"  Copper raw:    {copper_raw.shape[0]} rows, columns: {list(copper_raw.columns)}")
print(f"  Renewable raw: {renewable_raw.shape[0]} rows, columns: {list(renewable_raw.columns)}")


# ---------------------------------------------------------------------------
# 2. Clean copper prices (FRED format: DATE, VALUE)
#    - Parse the DATE column as a proper datetime
#    - Extract the year
#    - Drop any rows where VALUE is missing (FRED uses '.' for missing)
# ---------------------------------------------------------------------------

print("\nCleaning copper price data...")

copper = copper_raw.copy()

# FRED sometimes stores missing values as '.' — coerce these to NaN
copper.columns = copper.columns.str.strip()                    # remove accidental whitespace
copper.rename(columns={"observation_date": "date", "PCOPPUSDM": "copper_price_usd"}, inplace=True)

copper["date"]             = pd.to_datetime(copper["date"])
copper["copper_price_usd"] = pd.to_numeric(copper["copper_price_usd"], errors="coerce")
copper["year"]             = copper["date"].dt.year

# Report how many missing values exist before dropping
n_missing = copper["copper_price_usd"].isna().sum()
print(f"  Missing values in copper price column: {n_missing}")

copper.dropna(subset=["copper_price_usd"], inplace=True)
print(f"  Rows after dropping missing: {len(copper)}")
print(f"  Year range: {copper['year'].min()} – {copper['year'].max()}")


# ---------------------------------------------------------------------------
# 3. Aggregate monthly copper prices to annual means
#    Rationale: renewable capacity data is annual; we need matching frequency.
#    Using the mean of all months in a year is standard practice.
# ---------------------------------------------------------------------------

print("\nAggregating copper prices to annual means...")

copper_annual = (
    copper
    .groupby("year", as_index=False)["copper_price_usd"]
    .mean()
    .round(2)
)

print(f"  Annual copper series: {len(copper_annual)} years")


# ---------------------------------------------------------------------------
# 4. Clean renewable capacity data (IRENA format: Year, Value)
# ---------------------------------------------------------------------------

print("\nCleaning renewable capacity data...")

renewable = renewable_raw.copy()

# Skip the top title row by reloading with skiprows
renewable = pd.read_csv(RENEWABLE_FILE, skiprows=1)
renewable.columns = renewable.columns.str.strip()

# Rename the capacity column
renewable.rename(columns={
    "Year": "year",
    "Electricity capacity statistics": "renewable_gw"
}, inplace=True)

# Keep only global totals
renewable = renewable[
    (renewable["Region"] == "World") &
    (renewable["Technology"] == "Total renewable energy")
].copy()

# Coerce to numeric
renewable["year"]         = pd.to_numeric(renewable["year"], errors="coerce")
renewable["renewable_gw"] = pd.to_numeric(renewable["renewable_gw"], errors="coerce")

renewable.dropna(subset=["year", "renewable_gw"], inplace=True)
renewable["year"] = renewable["year"].astype(int)

# Convert MW to GW
renewable["renewable_gw"] = (renewable["renewable_gw"] / 1000).round(2)

print(f"  Year range: {renewable['year'].min()} – {renewable['year'].max()}")


# ---------------------------------------------------------------------------
# 5. Merge on year (inner join keeps only years present in both datasets)
# ---------------------------------------------------------------------------

print("\nMerging datasets on year...")

merged = pd.merge(copper_annual, renewable, on="year", how="inner")
merged.sort_values("year", inplace=True)
merged.reset_index(drop=True, inplace=True)

print(f"  Merged dataset: {len(merged)} years")
print(f"  Year range after merge: {merged['year'].min()} – {merged['year'].max()}")
print(f"  Columns: {list(merged.columns)}")


# ---------------------------------------------------------------------------
# 6. Final checks and save
# ---------------------------------------------------------------------------

print("\nFinal dataset summary:")
print(merged.describe())

# Check for any remaining missing values in the final dataset
total_missing = merged.isnull().sum().sum()
if total_missing > 0:
    print(f"\n  WARNING: {total_missing} missing values remain in merged dataset.")
    print(merged.isnull().sum())
else:
    print("\n  No missing values in merged dataset. Clean.")

merged.to_csv(OUTPUT_FILE, index=False)
print(f"\nClean data saved to: {OUTPUT_FILE}")
print("Stage 3 complete.")