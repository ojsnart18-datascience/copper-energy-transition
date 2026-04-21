# Copper and the Clean Energy Transition

A data-driven blog post examining whether the global shift towards renewable energy 
is reflected in copper prices, using data from FRED and IRENA covering 2006–2024.

**Blog post:** https://hackmd.io/@wHvrr12wRHuOrzgZXhyLYw/HkY_0A46bx

---

## How to Replicate

1. Clone the repository:
```bash
   git clone https://github.com/ojsnart18-datascience/copper-energy-transition.git
   cd copper-energy-transition
```

2. Install dependencies:
```bash
   pip install -r requirements.txt
```

3. Run the scripts in order:
```bash
   python src/02_clean.py
   python src/03_explore.py
   python src/04_regression.py
```

Running these three scripts in order will reproduce all cleaned data, figures, and regression outputs. All file paths are relative so no changes are needed after cloning.

---
## Project Structure

```
copper-energy-transition/
├── README.md
├── requirements.txt
├── blog.md                    ← full blog post in Markdown
├── data/
│   ├── raw/                   ← original downloaded data, never modified
│   └── clean/                 ← processed and merged data, ready for analysis
├── src/
│   ├── 02_clean.py            ← loads and cleans all five raw datasets
│   ├── 03_explore.py          ← produces exploratory figures
│   └── 04_regression.py       ← runs OLS regression models and saves outputs
└── output/
    ├── figures/               ← six saved PNG figures
    └── tables/                ← regression results table
```

---

## Data Sources

- **Copper prices:** FRED, series `PCOPPUSDM` — monthly global copper price in USD per tonne (IMF Primary Commodity Prices)
- **Renewable energy capacity:** IRENA Electricity Capacity Statistics — annual installed capacity in GW
- **World GDP growth:** FRED, series `NYGDPPCAPKDWLD` — World Bank annual GDP per capita, used to compute growth rate
- **US Dollar Index:** FRED, series `DTWEXBGS` — broad trade-weighted dollar index, daily averaged to annual

---

## Author

Oliver Snart — University of Exeter, BEE2041 Data Science in Economics, 2026