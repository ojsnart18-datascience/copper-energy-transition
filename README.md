# Copper and the Clean Energy Transition

A data-driven blog post examining whether the global shift towards 
renewable energy is reflected in the increase in copper prices, using data from 
FRED and IRENA covering 1990–2023.

**Blog post:** [Link to be added once published]

---

## Project Structure

copper-energy-transition/
├── README.md
├── requirements.txt
├── data/
│   ├── raw/        ← original downloaded data, never modified
│   └── clean/      ← processed and merged data, ready for analysis
├── src/
│   ├── 01_clean.py       ← loads and cleans raw data
│   ├── 02_analysis.py    ← runs regression model
│   └── 03_figures.py     ← produces all plots
├── output/
│   ├── figures/    ← saved PNG plots
│   └── tables/     ← regression output
└── blog.ipynb      ← full blog post with narrative and embedded figures

## Data Sources

- **Copper prices:** FRED (Federal Reserve Economic Data), 
  series `PCOPPUSDM` — monthly global copper price in USD per metric tonne
- **Renewable energy capacity:** IRENA Renewable Capacity Statistics — 
  annual installed capacity (GW) by technology and country

## How to Replicate This Project

1. Clone this repository:
```bash
git clone https://github.com/ojsnart18-datascience/copper-energy-transition.git
cd copper-energy-transition
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run scripts in order:
```bash
python src/01_clean.py
python src/02_analysis.py
python src/03_figures.py
```

4. Open the blog:
```bash
jupyter notebook blog.ipynb
```

## Author

Oliver Snart — University of Exeter, BEE2041 Data Science in Economics, 2026
