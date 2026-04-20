"""
04_regression.py
----------------
Stage 5: OLS Regression Analysis
BEE2041 Empirical Project — Green Copper

What this script does:
  1. Loads the clean merged dataset
  2. Runs two OLS regressions:
     - Model 1: Copper price on renewable capacity alone (baseline)
     - Model 2: Copper price on renewable capacity + GDP growth + dollar index
       Note: Oil price was tested but removed due to multicollinearity with
       GDP growth and statistical insignificance (p=0.336)
  3. Prints full regression summaries for both models
  4. Saves two figures:
     - Figure 5: Model comparison bar chart (R-squared improvement)
     - Figure 6: Actual vs fitted values from Model 2
  5. Saves a results comparison table to output/tables/

Input:
  data/clean/merged_clean.csv

Outputs:
  output/figures/fig5_model_comparison.png
  output/figures/fig6_actual_vs_fitted.png
  output/tables/regression_summary.csv
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import statsmodels.api as sm
import os

# ---------------------------------------------------------------------------
# 0. Paths
# ---------------------------------------------------------------------------

CLEAN_FILE  = os.path.join("data", "clean", "merged_clean.csv")
FIGURES_DIR = os.path.join("output", "figures")
TABLES_DIR  = os.path.join("output", "tables")

os.makedirs(FIGURES_DIR, exist_ok=True)
os.makedirs(TABLES_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# 1. Load clean data
# ---------------------------------------------------------------------------

print("Loading clean data...")
df = pd.read_csv(CLEAN_FILE)
print(f"  {len(df)} observations loaded, {df['year'].min()}–{df['year'].max()}")

# ---------------------------------------------------------------------------
# 2. Define variables
#    Y  = copper price (dependent variable)
#    X1 = renewable capacity only (baseline model)
#    X2 = renewable capacity + GDP growth + dollar index (full model)
#
#    Note: oil price was tested and removed. It was statistically
#    insignificant (p=0.336) and correlated with GDP growth, causing
#    multicollinearity. Removing it produces a cleaner, more stable model.
# ---------------------------------------------------------------------------

Y  = df["copper_price_usd"]
X1 = sm.add_constant(df[["renewable_gw"]])
X2 = sm.add_constant(df[["renewable_gw", "gdp_growth_pct", "dollar_index"]])

# ---------------------------------------------------------------------------
# 3. Run both OLS regressions
# ---------------------------------------------------------------------------

print("\n" + "="*60)
print("MODEL 1: Baseline (renewable capacity only)")
print("="*60)
result1 = sm.OLS(Y, X1).fit()
print(result1.summary())

print("\n" + "="*60)
print("MODEL 2: Full model (renewable + GDP growth + dollar index)")
print("="*60)
result2 = sm.OLS(Y, X2).fit()
print(result2.summary())

# Key values
coef_renewable = result2.params["renewable_gw"]
coef_gdp       = result2.params["gdp_growth_pct"]
coef_dollar    = result2.params["dollar_index"]
r2_model1      = result1.rsquared
r2_model2      = result2.rsquared
p_renewable    = result2.pvalues["renewable_gw"]
p_gdp          = result2.pvalues["gdp_growth_pct"]
p_dollar       = result2.pvalues["dollar_index"]

print("\n--- Plain English Interpretation (Model 2) ---")
print(f"  Renewable capacity: +1 GW → ${coef_renewable:.2f} change in copper price (p={p_renewable:.4f})")
print(f"  GDP growth:         +1%  → ${coef_gdp:.2f} change in copper price (p={p_gdp:.4f})")
print(f"  Dollar index:       +1pt → ${coef_dollar:.2f} change in copper price (p={p_dollar:.4f})")
print(f"\n  Model 1 R²: {r2_model1:.3f}")
print(f"  Model 2 R²: {r2_model2:.3f}")

# ---------------------------------------------------------------------------
# 4. Save comparison table
# ---------------------------------------------------------------------------

results_df = pd.DataFrame({
    "Variable": ["Renewable Capacity (GW)", "GDP Growth (%)",
                 "Dollar Index", "Constant", "R-squared", "Observations"],
    "Model 1 (Baseline)": [
        f"{result1.params['renewable_gw']:.4f} (p={result1.pvalues['renewable_gw']:.3f})",
        "—", "—",
        f"{result1.params['const']:.2f}",
        f"{r2_model1:.3f}",
        len(df)
    ],
    "Model 2 (Full)": [
        f"{result2.params['renewable_gw']:.4f} (p={result2.pvalues['renewable_gw']:.3f})",
        f"{result2.params['gdp_growth_pct']:.4f} (p={result2.pvalues['gdp_growth_pct']:.3f})",
        f"{result2.params['dollar_index']:.4f} (p={result2.pvalues['dollar_index']:.3f})",
        f"{result2.params['const']:.2f}",
        f"{r2_model2:.3f}",
        len(df)
    ]
})

results_df.to_csv(os.path.join(TABLES_DIR, "regression_summary.csv"), index=False)
print(f"\n  Results table saved to output/tables/regression_summary.csv")

# ---------------------------------------------------------------------------
# 5. Figure 5 — Model comparison bar chart
# ---------------------------------------------------------------------------

print("\nProducing Figure 5: Model comparison bar chart...")

fig, ax = plt.subplots(figsize=(8, 5))

models    = ["Model 1\n(Renewable Only)", "Model 2\n(Full Model)"]
r2_values = [r2_model1, r2_model2]
colours   = ["#a8c5a0", "#2a7d4f"]

bars = ax.bar(models, r2_values, color=colours, width=0.4, edgecolor="white")

for bar, val in zip(bars, r2_values):
    ax.text(bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.01,
            f"R² = {val:.3f}",
            ha="center", va="bottom", fontsize=12, fontweight="bold")

ax.set_ylim(0, 1.05)
ax.set_ylabel("R-squared (Explanatory Power)", fontsize=12)
ax.set_title("Adding Control Variables Dramatically Improves the Model",
             fontsize=13, fontweight="bold", pad=12)

ax.text(0.5, 0.5,
        "Model 2 explains 83% of copper\nprice variation vs 19% for Model 1",
        transform=ax.transAxes,
        fontsize=10, ha="center", va="center", color="dimgray",
        bbox=dict(boxstyle="round,pad=0.4", facecolor="#f9f9f9", edgecolor="lightgray"))

plt.tight_layout()
fig.savefig(os.path.join(FIGURES_DIR, "fig5_model_comparison.png"))
plt.close()
print("  Saved fig5_model_comparison.png")

# ---------------------------------------------------------------------------
# 6. Figure 6 — Actual vs fitted values from Model 2
# ---------------------------------------------------------------------------

print("Producing Figure 6: Actual vs fitted values...")

fitted_values = result2.fittedvalues

fig, ax = plt.subplots(figsize=(10, 6))

ax.plot(df["year"], df["copper_price_usd"], color="#2a7d4f", linewidth=2.5,
        marker="o", markersize=5, label="Actual Copper Price")

ax.plot(df["year"], fitted_values, color="#b5451b", linewidth=2.5,
        linestyle="--", marker="s", markersize=5, label="Model 2 Fitted Values")

results_text = (f"Model 2 Results\n"
                f"R² = {r2_model2:.3f}\n"
                f"Renewable β = ${coef_renewable:.2f}/GW\n"
                f"p = {p_renewable:.4f}")
ax.text(0.02, 0.97, results_text,
        transform=ax.transAxes, fontsize=9, verticalalignment="top",
        bbox=dict(boxstyle="round,pad=0.4", facecolor="white", edgecolor="gray", alpha=0.8))

ax.set_title("Actual vs Fitted Copper Prices: Full OLS Model, 2006–2024",
             fontsize=13, fontweight="bold", pad=12)
ax.set_xlabel("Year", fontsize=12)
ax.set_ylabel("Copper Price (USD per tonne)", fontsize=12)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
ax.set_xlim(df["year"].min() - 0.5, df["year"].max() + 0.5)
ax.legend(fontsize=10)

plt.tight_layout()
fig.savefig(os.path.join(FIGURES_DIR, "fig6_actual_vs_fitted.png"))
plt.close()
print("  Saved fig6_actual_vs_fitted.png")

print("\nStage 5 complete.")