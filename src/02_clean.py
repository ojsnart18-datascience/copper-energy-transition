"""
02_clean.py
-----------
Stage 3: Data Cleaning and Merging
BEE2041 Empirical Project — Green Copper

What this script does:
  1. Loads five raw datasets:
     - Copper prices (FRED, monthly)
     - Renewable energy capacity (IRENA, annual)
     - World GDP per capita (FRED, annual)
     - Brent crude oil price (FRED, monthly)
     - US Dollar Index (FRED, daily)
  2. Cleans and aggregates each to annual frequency
  3. Computes world GDP growth rate from GDP per capita levels
  4. Merges all five on year (inner join)
  5. Saves one clean CSV to data/clean/merged_clean.csv

Inputs:
  data/raw/copper_prices.csv
  data/raw/renewable_capacity.csv
  data/raw/world_gdp_growth.csv
  data/raw/brent_oil_price.csv
  data/raw/us_dollar_index.csv

Output:
  data/clean/merged_clean.csv
"""

import pandas as pd
import os

# ---------------------------------------------------------------------------
# 0. Paths
# ---------------------------------------------------------------------------

RAW_DIR   = os.path.join("data", "raw")
CLEAN_DIR = os.path.join("data", "clean")
OUTPUT_FILE = os.path.join(CLEAN_DIR, "merged_clean.csv")

os.makedirs(CLEAN_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# 1. Copper prices (FRED, monthly) → annual mean
# ---------------------------------------------------------------------------

print("Loading and cleaning copper prices...")

copper = pd.read_csv(os.path.join(RAW_DIR, "copper_prices.csv"))
copper.columns = copper.columns.str.strip()
copper.rename(columns={"observation_date": "date", "PCOPPUSDM": "copper_price_usd"}, inplace=True)
copper["date"] = pd.to_datetime(copper["date"])
copper["copper_price_usd"] = pd.to_numeric(copper["copper_price_usd"], errors="coerce")
copper["year"] = copper["date"].dt.year
copper.dropna(subset=["copper_price_usd"], inplace=True)

copper_annual = (
    copper.groupby("year", as_index=False)["copper_price_usd"]
    .mean()
    .round(2)
)
print(f"  Copper: {len(copper_annual)} annual observations, {copper_annual['year'].min()}–{copper_annual['year'].max()}")

# ---------------------------------------------------------------------------
# 2. Renewable energy capacity (IRENA, annual) → keep global totals, convert MW to GW
# ---------------------------------------------------------------------------

print("Loading and cleaning renewable capacity...")

renewable = pd.read_csv(os.path.join(RAW_DIR, "renewable_capacity.csv"), skiprows=1)
renewable.columns = renewable.columns.str.strip()
renewable.rename(columns={
    "Year": "year",
    "Electricity capacity statistics": "renewable_gw"
}, inplace=True)

renewable = renewable[
    (renewable["Region"] == "World") &
    (renewable["Technology"] == "Total renewable energy")
].copy()

renewable["year"] = pd.to_numeric(renewable["year"], errors="coerce")
renewable["renewable_gw"] = pd.to_numeric(renewable["renewable_gw"], errors="coerce")
renewable.dropna(subset=["year", "renewable_gw"], inplace=True)
renewable["year"] = renewable["year"].astype(int)
renewable["renewable_gw"] = (renewable["renewable_gw"] / 1000).round(2)
renewable = renewable[["year", "renewable_gw"]]
print(f"  Renewable: {len(renewable)} annual observations, {renewable['year'].min()}–{renewable['year'].max()}")

# ---------------------------------------------------------------------------
# 3. World GDP per capita (FRED, annual) → compute annual growth rate (%)
# ---------------------------------------------------------------------------

print("Loading and cleaning world GDP growth...")

gdp = pd.read_csv(os.path.join(RAW_DIR, "world_gdp_growth.csv"))
gdp.columns = gdp.columns.str.strip()
gdp.rename(columns={"observation_date": "date", "NYGDPPCAPKDWLD": "gdp_per_capita"}, inplace=True)
gdp["date"] = pd.to_datetime(gdp["date"])
gdp["year"] = gdp["date"].dt.year
gdp["gdp_per_capita"] = pd.to_numeric(gdp["gdp_per_capita"], errors="coerce")
gdp.dropna(subset=["gdp_per_capita"], inplace=True)
gdp.sort_values("year", inplace=True)

# Compute percentage growth rate year on year
gdp["gdp_growth_pct"] = gdp["gdp_per_capita"].pct_change() * 100
gdp = gdp[["year", "gdp_growth_pct"]].dropna()
gdp["gdp_growth_pct"] = gdp["gdp_growth_pct"].round(3)
print(f"  GDP growth: {len(gdp)} annual observations, {gdp['year'].min()}–{gdp['year'].max()}")

# ---------------------------------------------------------------------------
# 4. Brent crude oil price (FRED, monthly) → annual mean
# ---------------------------------------------------------------------------

print("Loading and cleaning Brent oil price...")

oil = pd.read_csv(os.path.join(RAW_DIR, "brent_oil_price.csv"))
oil.columns = oil.columns.str.strip()
oil.rename(columns={"observation_date": "date", "POILBREUSDM": "oil_price_usd"}, inplace=True)
oil["date"] = pd.to_datetime(oil["date"])
oil["oil_price_usd"] = pd.to_numeric(oil["oil_price_usd"], errors="coerce")
oil["year"] = oil["date"].dt.year
oil.dropna(subset=["oil_price_usd"], inplace=True)

oil_annual = (
    oil.groupby("year", as_index=False)["oil_price_usd"]
    .mean()
    .round(2)
)
print(f"  Oil price: {len(oil_annual)} annual observations, {oil_annual['year'].min()}–{oil_annual['year'].max()}")

# ---------------------------------------------------------------------------
# 5. US Dollar Index (FRED, daily) → annual mean
# ---------------------------------------------------------------------------

print("Loading and cleaning US Dollar Index...")

dollar = pd.read_csv(os.path.join(RAW_DIR, "us_dollar_index.csv"))
dollar.columns = dollar.columns.str.strip()
dollar.rename(columns={"observation_date": "date", "DTWEXBGS": "dollar_index"}, inplace=True)
dollar["date"] = pd.to_datetime(dollar["date"])
dollar["dollar_index"] = pd.to_numeric(dollar["dollar_index"], errors="coerce")
dollar["year"] = dollar["date"].dt.year
dollar.dropna(subset=["dollar_index"], inplace=True)

dollar_annual = (
    dollar.groupby("year", as_index=False)["dollar_index"]
    .mean()
    .round(2)
)
print(f"  Dollar index: {len(dollar_annual)} annual observations, {dollar_annual['year'].min()}–{dollar_annual['year'].max()}")

# ---------------------------------------------------------------------------
# 6. Merge all five datasets on year (inner join)
#    Inner join keeps only years present in ALL datasets
# ---------------------------------------------------------------------------

print("\nMerging all datasets on year...")

merged = copper_annual.copy()
merged = pd.merge(merged, renewable,     on="year", how="inner")
merged = pd.merge(merged, gdp,           on="year", how="inner")
merged = pd.merge(merged, oil_annual,    on="year", how="inner")
merged = pd.merge(merged, dollar_annual, on="year", how="inner")

merged.sort_values("year", inplace=True)
merged.reset_index(drop=True, inplace=True)

print(f"  Final dataset: {len(merged)} years")
print(f"  Year range: {merged['year'].min()}–{merged['year'].max()}")
print(f"  Columns: {list(merged.columns)}")

# ---------------------------------------------------------------------------
# 7. Final checks and save
# ---------------------------------------------------------------------------

print("\nFinal dataset summary:")
print(merged.describe().round(2))

total_missing = merged.isnull().sum().sum()
if total_missing > 0:
    print(f"\n  WARNING: {total_missing} missing values remain.")
    print(merged.isnull().sum())
else:
    print("\n  No missing values. Clean.")

merged.to_csv(OUTPUT_FILE, index=False)
print(f"\nClean data saved to: {OUTPUT_FILE}")
print("Stage 3 complete.")