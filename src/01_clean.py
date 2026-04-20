import pandas as pd

# ── COPPER PRICES ──────────────────────────────────────────
copper = pd.read_csv('data/raw/copper_prices.csv')

print("=== COPPER DATA ===")
print("Shape:", copper.shape)
print("\nFirst 5 rows:")
print(copper.head())
print("\nColumn names:")
print(copper.columns.tolist())

# ── RENEWABLE ENERGY CAPACITY ───────────────────────────────
irena = pd.read_csv('data/raw/renewable_energy_capacity.csv', skiprows=2)

print("\n=== IRENA DATA ===")
print("Shape:", irena.shape)
print("\nFirst 5 rows:")
print(irena.head())
print("\nColumn names:")
print(irena.columns.tolist())
print("\nData types:")
print(irena.dtypes)
       
