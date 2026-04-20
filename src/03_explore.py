"""
03_explore.py
-------------
Stage 4: Exploratory Analysis and Figures
BEE2041 Empirical Project — Green Copper

What this script does:
  1. Loads the clean merged dataset
  2. Produces four publication-quality figures saved to output/figures/
     - Figure 1: Copper price time series (2000-2025)
     - Figure 2: Global renewable capacity time series (2000-2025)
     - Figure 3: Dual-axis chart showing both variables together
     - Figure 4: Scatter plot of renewable capacity vs copper price

Input:
  data/clean/merged_clean.csv

Outputs:
  output/figures/fig1_copper_prices.png
  output/figures/fig2_renewable_capacity.png
  output/figures/fig3_dual_axis.png
  output/figures/fig4_scatter.png
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import os

# ---------------------------------------------------------------------------
# 0. Settings and paths
# ---------------------------------------------------------------------------

# Use a clean, minimal style throughout
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams["figure.dpi"] = 150
plt.rcParams["font.size"]  = 11

CLEAN_FILE  = os.path.join("data", "clean", "merged_clean.csv")
FIGURES_DIR = os.path.join("output", "figures")

os.makedirs(FIGURES_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# 1. Load clean data
# ---------------------------------------------------------------------------

print("Loading clean data...")
df = pd.read_csv(CLEAN_FILE)
print(f"  {len(df)} rows loaded, columns: {list(df.columns)}")
print(df.head())

# ---------------------------------------------------------------------------
# 2. Figure 1 — Copper price time series
# ---------------------------------------------------------------------------

print("\nProducing Figure 1: Copper price time series...")

fig, ax = plt.subplots(figsize=(10, 5))

ax.plot(df["year"], df["copper_price_usd"], color="#b5451b", linewidth=2.5, marker="o", markersize=4)

ax.set_title("Global Copper Prices, 2000–2025", fontsize=14, fontweight="bold", pad=12)
ax.set_xlabel("Year", fontsize=12)
ax.set_ylabel("Price (USD per tonne)", fontsize=12)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
ax.set_xlim(df["year"].min() - 0.5, df["year"].max() + 0.5)

# Annotate the 2011 peak and 2016 trough as they tell a story
peak_year = df.loc[df["copper_price_usd"].idxmax(), "year"]
peak_val  = df["copper_price_usd"].max()
ax.annotate(f"Peak: ${peak_val:,.0f}\n({peak_year})",
            xy=(peak_year, peak_val),
            xytext=(peak_year - 4, peak_val - 800),
            arrowprops=dict(arrowstyle="->", color="black"),
            fontsize=9)

plt.tight_layout()
fig.savefig(os.path.join(FIGURES_DIR, "fig1_copper_prices.png"))
plt.close()
print("  Saved fig1_copper_prices.png")

# ---------------------------------------------------------------------------
# 3. Figure 2 — Renewable capacity time series
# ---------------------------------------------------------------------------

print("Producing Figure 2: Renewable capacity time series...")

fig, ax = plt.subplots(figsize=(10, 5))

ax.plot(df["year"], df["renewable_gw"], color="#2a7d4f", linewidth=2.5, marker="o", markersize=4)
ax.fill_between(df["year"], df["renewable_gw"], alpha=0.15, color="#2a7d4f")

ax.set_title("Global Renewable Energy Capacity, 2000–2025", fontsize=14, fontweight="bold", pad=12)
ax.set_xlabel("Year", fontsize=12)
ax.set_ylabel("Installed Capacity (GW)", fontsize=12)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f} GW"))
ax.set_xlim(df["year"].min() - 0.5, df["year"].max() + 0.5)

plt.tight_layout()
fig.savefig(os.path.join(FIGURES_DIR, "fig2_renewable_capacity.png"))
plt.close()
print("  Saved fig2_renewable_capacity.png")

# ---------------------------------------------------------------------------
# 4. Figure 3 — Dual-axis chart (both variables together)
# ---------------------------------------------------------------------------

print("Producing Figure 3: Dual-axis chart...")

fig, ax1 = plt.subplots(figsize=(11, 5))

colour_copper    = "#b5451b"
colour_renewable = "#2a7d4f"

# Left axis — copper price
ax1.plot(df["year"], df["copper_price_usd"], color=colour_copper,
         linewidth=2.5, marker="o", markersize=4, label="Copper Price")
ax1.set_xlabel("Year", fontsize=12)
ax1.set_ylabel("Copper Price (USD per tonne)", fontsize=12, color=colour_copper)
ax1.tick_params(axis="y", labelcolor=colour_copper)
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))

# Right axis — renewable capacity
ax2 = ax1.twinx()
ax2.plot(df["year"], df["renewable_gw"], color=colour_renewable,
         linewidth=2.5, marker="s", markersize=4, linestyle="--", label="Renewable Capacity")
ax2.set_ylabel("Renewable Capacity (GW)", fontsize=12, color=colour_renewable)
ax2.tick_params(axis="y", labelcolor=colour_renewable)
ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f} GW"))

# Combined legend
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left", fontsize=10)

ax1.set_title("Copper Prices and Renewable Energy Capacity, 2000–2025",
              fontsize=14, fontweight="bold", pad=12)
ax1.set_xlim(df["year"].min() - 0.5, df["year"].max() + 0.5)

plt.tight_layout()
fig.savefig(os.path.join(FIGURES_DIR, "fig3_dual_axis.png"))
plt.close()
print("  Saved fig3_dual_axis.png")

# ---------------------------------------------------------------------------
# 5. Figure 4 — Scatter plot: renewable capacity vs copper price
# ---------------------------------------------------------------------------

print("Producing Figure 4: Scatter plot...")

fig, ax = plt.subplots(figsize=(8, 6))

scatter = ax.scatter(df["renewable_gw"], df["copper_price_usd"],
                     color="#3365da", s=80, zorder=3)

# Label each point with its year
for _, row in df.iterrows():
    ax.annotate(str(int(row["year"])),
                xy=(row["renewable_gw"], row["copper_price_usd"]),
                xytext=(4, 4), textcoords="offset points",
                fontsize=7, color="dimgray")


ax.set_title("Renewable Capacity vs Copper Price, 2000–2025",
             fontsize=14, fontweight="bold", pad=12)
ax.set_xlabel("Renewable Capacity (GW)", fontsize=12)
ax.set_ylabel("Copper Price (USD per tonne)", fontsize=12)
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f} GW"))
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))

plt.tight_layout()
fig.savefig(os.path.join(FIGURES_DIR, "fig4_scatter.png"))
plt.close()
print("  Saved fig4_scatter.png")

# ---------------------------------------------------------------------------
# 6. Print summary statistics for reference in blog writing
# ---------------------------------------------------------------------------

print("\n--- Summary Statistics ---")
print(df[["copper_price_usd", "renewable_gw"]].describe().round(2))

print("\n--- Correlation ---")
corr = df["copper_price_usd"].corr(df["renewable_gw"])
print(f"  Pearson correlation between copper price and renewable capacity: {corr:.3f}")

print("\nStage 4 complete. Four figures saved to output/figures/")