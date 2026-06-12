# Malaysia COVID-19 Data Analysis

A Python script for university statistics project — analyzes Malaysia COVID-19 cases, deaths, and testing data from the Ministry of Health.

---

## Project Structure

```
PROJECT/
├── covid_analysis.py       # Main analysis script
├── README.md               # This file
├── DATASETS/
│   ├── malaysia_covid_cases.csv
│   ├── malaysia_covid_deaths.csv
│   └── malaysia_covid_tests.csv
├── descriptive_stats.csv   # Output: table of statistics
├── daily_new_cases_line.png     # Output: line chart
├── tests_vs_cases_scatter.png   # Output: scatter plot
└── monthly_cases_deaths_bar.png # Output: bar chart
```

---

## Requirements

- **Python 3** installed on your system
- Internet connection (first run only — installs packages)

---

## How to Run

### 1. Open a terminal / command prompt

- **Windows**: Press `Win + R`, type `cmd`, press Enter
- **macOS / Linux**: Open the Terminal app

### 2. Navigate to the project folder

```bash
cd /mnt/d/Temp/PROJECT
```

### 3. Run the script

```bash
python3 covid_analysis.py
```

> If `python3` doesn't work, try `python covid_analysis.py`

The script will **automatically install** pandas, matplotlib, scipy, and scikit-learn on the first run.

---

## What the Script Does (Step by Step)

| Section | What it computes | Output |
|---|---|---|
| **1. Load & Merge** | Reads all 3 CSV files and joins them by date | — |
| **2. Clean** | Converts dates, computes `total_tests`, drops missing rows | Console message |
| **3. Descriptive Stats** | Mean, median, mode, std dev, variance, min, max | Console table + `descriptive_stats.csv` |
| **4. Visualizations** | Line chart, scatter plot, monthly bar chart | 3 PNG files |
| **5. Inferential Stats** | Linear regression (deaths ~ cases), Pearson correlation with hypothesis test | Console |
| **6. Bonus** | Positivity rate analysis, regression (deaths ~ positivity rate) | Console |

---

## Output Files for Your Report

| File | What to do with it |
|---|---|
| `descriptive_stats.csv` | Copy the numbers into your **Descriptive Statistics** table |
| `daily_new_cases_line.png` | Insert into **Data Visualization** section |
| `tests_vs_cases_scatter.png` | Insert into **Data Visualization** section |
| `monthly_cases_deaths_bar.png` | Insert into **Data Visualization** section |
| Console output | Copy regression/correlation values into **Inferential Statistics** section |

---

## Key Results (from the analysis)

| Metric | New Cases | New Deaths | Total Tests |
|---|---|---|---|
| Mean | 2,810.78 | 19.64 | 38,346.78 |
| Median | 517.5 | 1.0 | 11,313.5 |
| Std Dev | 5,408.87 | 56.29 | 52,995.60 |

**Regression (deaths ~ cases):** Coefficient = 0.0074, R² = 0.500

**Pearson correlation:** r = 0.707, p ≈ 2.4×10⁻²⁸⁸ → **Reject H₀** (significant relationship at α = 0.05)

**Positivity rate:** Mean = 8.84%, R² = 0.003 (weak predictor)

---

## Report Sections Mapped to Script Outputs

| Report Section | Where the data comes from |
|---|---|
| Introduction | Describe the dataset and purpose |
| Case Study Discussion | Explain COVID-19 in Malaysia context |
| Concepts Used | List statistics formulas used |
| Data Construction | Explain merge, cleaning steps |
| Programming Code | Reference `covid_analysis.py` |
| Analysis of Results | Copy numbers from console + CSV |
| Discussion/Conclusion | Interpret the findings |
| Appendix | Attach rubric + peer evaluation form |

---

## Troubleshooting

**"python3 not found"** → Try `python` instead of `python3`

**"No module named pandas"** → Run `pip3 install pandas matplotlib scipy scikit-learn` manually

**Permission error on install** → Add `--break-system-packages` to the pip command (Linux) or run terminal as Administrator (Windows)
