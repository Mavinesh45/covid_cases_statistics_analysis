# Malaysia COVID-19 Analysis — Complete Findings Reference

All values, outputs, and interpretations from the analysis for use in your project report.

---

## 1. DATA OVERVIEW

### Source
Malaysia Ministry of Health (MOH) — publicly available COVID-19 data from GitHub.

### Files Used

| File | Rows | Columns Kept | Date Range |
|---|---|---|---|
| `malaysia_covid_cases.csv` | 1955 | `date`, `cases_new` | 25 Jan 2020 – ~Jun 2026 |
| `malaysia_covid_deaths.csv` | 1903 | `date`, `deaths_new` | 17 Mar 2020 – ~Jun 2026 |
| `malaysia_covid_tests.csv` | 1956 | `date`, `rtk-ag`, `pcr` | 24 Jan 2020 – ~Jun 2026 |

### After Cleaning
- **Total rows:** 1955 → 1,902 (53 rows dropped due to missing values)
- **Key columns:** `cases_new`, `deaths_new`, `total_tests` (= `rtk-ag` + `pcr`)
- **Derived columns:** `positivity_rate`, `month`

---

## 2. DESCRIPTIVE STATISTICS

### Table of Values

| Variable | Mean | Median | Mode | Std Dev | Variance | Min | Max |
|---|---|---|---|---|---|---|---|
| **New Cases** | 2,810.78 | 517.5 | 6.0 | 5,408.87 | 29,255,860 | 1 | 33,406 |
| **New Deaths** | 19.64 | 1.0 | 0.0 | 56.29 | 3,168.37 | 0 | 592 |
| **Total Tests** | 38,346.78 | 11,313.5 | 405.0 | 52,995.60 | 2,808,533,000 | 42 | 297,765 |

### Interpretation Notes for Report

- **New Cases (mean = 2,810.78):** On average, ~2,811 new cases per day. The **median (517.5)** is much lower than the mean — this tells you the data is **right-skewed** (many low-value days pulled up by a few massive spikes).
- **New Deaths (mean = 19.64):** Average ~20 deaths/day. Mode = 0 means most days had no deaths. Std dev (56.29) is nearly 3× the mean → highly volatile.
- **Total Tests (mean = 38,346.78):** Average ~38K tests/day. The huge range (42 – 297,765) reflects testing ramping up over time.
- **Variance:** Cases variance (29 million) is enormous — confirms extreme fluctuation across waves.

---

## 3. DATA VISUALIZATIONS

### 3a. Daily New Cases Line Chart
**File:** `daily_new_cases_line.png`

- **What it shows:** A time-series line of `cases_new` across all dates.
- **Key patterns visible:**
  - Multiple **waves** (peaks) corresponding to Delta, Omicron, etc.
  - Early 2020: near-zero cases
  - Mid-2021: first major spike (Delta wave)
  - Early 2022: largest spike (Omicron wave) — peaked at **33,406 cases**
  - Late 2022 onward: declining trend with small fluctuations

### 3b. Total Tests vs New Cases Scatter Plot
**File:** `tests_vs_cases_scatter.png`

- **What it shows:** Each dot = one day; x-axis = tests performed, y-axis = new cases detected.
- **Pattern:** Positive correlation — more testing tends to find more cases, but the relationship weakens at higher test volumes (spread increases).

### 3c. Monthly Cases and Deaths Bar Chart
**File:** `monthly_cases_deaths_bar.png`

- **Dual y-axes:** Left (red) = monthly cases, Right (blue) = monthly deaths.
- **Observation:** Cases and deaths move together but deaths lag slightly behind case peaks (as expected — people die after being infected).

---

## 4. INFERENTIAL STATISTICS

### 4a. Linear Regression: Deaths ~ Cases

| Statistic | Value |
|---|---|
| **Coefficient (slope)** | 0.007359 |
| **Intercept** | -1.046976 |
| **R-squared** | 0.5001 |

**Interpretation:**
- **Coefficient = 0.0074:** For every additional 1 new case, deaths increase by ~0.0074. Or, for every **1,000 new cases**, expect ~7.4 more deaths.
- **Intercept = -1.05:** When cases = 0, predicted deaths ≈ -1 (essentially 0 — intercept has no real-world meaning here).
- **R² = 0.500:** 50% of the variation in deaths is explained by cases. The other 50% depends on other factors (vaccination, healthcare capacity, variant severity, etc.).

**Regression equation:**
```
deaths_new = 0.007359 × cases_new − 1.046976
```

### 4b. Pearson Correlation

| Statistic | Value |
|---|---|
| **Pearson r** | 0.707151 |
| **p-value** | 2.416341 × 10⁻²⁸⁸ |
| **Alpha (α)** | 0.05 |

**Interpretation:**
- **r = 0.707:** Strong **positive** linear correlation between cases and deaths.
- **p-value ≈ 2.4×10⁻²⁸⁸:** Extremely small (far below 0.05).
- **Conclusion: REJECT H₀** — There is statistically significant evidence of a linear relationship between new cases and new deaths.

**Hypothesis test wording for report:**
> H₀: ρ = 0 (no linear correlation between cases and deaths)  
> H₁: ρ ≠ 0 (linear correlation exists)  
> Since p-value (2.42e-288) < α (0.05), we reject the null hypothesis.  
> There is sufficient evidence to conclude a significant linear relationship exists between daily new COVID-19 cases and daily new deaths in Malaysia.

---

## 5. TEST POSITIVITY RATE

**Formula:** `positivity_rate = (cases_new / total_tests) × 100`

| Statistic | Value |
|---|---|
| **Mean positivity rate** | 8.84% |
| **Regression coefficient** | 0.312474 |
| **Intercept** | 16.874750 |
| **R-squared** | 0.002806 |

**Interpretation:**
- **Mean 8.84%:** On average, ~8.8% of tests returned positive. WHO recommends positivity <5% for adequate testing — Malaysia's average exceeds this, suggesting periods of under-testing.
- **R² = 0.003:** Positivity rate is a **very weak** predictor of deaths. Only 0.28% of death variation is explained by positivity rate.
- **Why?** Positivity rate depends on testing volume — when testing is low, positivity can be high even with few cases, making it a poor proxy for true infection burden.

---

## 6. PRACTICAL INSIGHTS & RECOMMENDATIONS

### Key Takeaways

1. **Cases drive deaths (R² = 0.50):** Reducing case numbers is strongly associated with fewer deaths — supports lockdowns/vaccination as life-saving measures.
2. **Testing matters:** The wide spread in the tests-vs-cases scatter plot suggests testing capacity was inconsistent.
3. **Positivity rate >5%:** Indicates possible under-testing during certain periods, especially during surge weeks.

### For Your Report's Conclusion

- The strong correlation (r = 0.707) between cases and deaths validates that case counts are a meaningful proxy for pandemic severity.
- The moderate R² (0.50) leaves room for other factors — discuss vaccination rollouts, healthcare system pressure, and variant differences.
- Malaysia experienced 3+ distinct waves — reference these in your case study discussion.

---

## 7. GLOSSARY OF TERMS FOR REPORT

| Term | Definition |
|---|---|
| **Mean** | Average value = sum ÷ count |
| **Median** | Middle value when sorted |
| **Mode** | Most frequent value |
| **Standard deviation** | How spread out values are from the mean |
| **Variance** | Standard deviation squared |
| **R-squared** | Proportion of variance in Y explained by X (0 to 1) |
| **Pearson r** | Strength and direction of linear relationship (−1 to +1) |
| **p-value** | Probability of observing data if H₀ is true |
| **α (alpha)** | Significance threshold (0.05 = 5% risk of Type I error) |
| **H₀ (null hypothesis)** | No effect / no relationship |
| **H₁ (alternative)** | There is an effect / relationship |
| **Positivity rate** | % of tests that are positive |

---

## 8. QUICK COPY-PASTE BLOCKS FOR REPORT

### Descriptive Statistics Paragraph
> "The dataset contains 1,902 days of data after cleaning. The mean daily new cases was 2,810.78 (SD = 5,408.87), with a median of 517.5 and a range of 1 to 33,406. New deaths averaged 19.64 per day (SD = 56.29), while total tests averaged 38,346.78 (SD = 52,995.60). The large difference between mean and median for cases indicates a right-skewed distribution driven by pandemic waves."

### Regression Paragraph
> "A linear regression was performed with deaths_new as the dependent variable and cases_new as the independent variable. The regression equation was deaths = 0.0074(cases) − 1.05. The coefficient indicates that each additional 1,000 cases is associated with approximately 7.4 additional deaths. The R-squared value of 0.500 suggests that cases explain 50% of the variance in deaths."

### Correlation Paragraph
> "Pearson correlation analysis revealed a strong positive relationship between daily new cases and daily new deaths (r = 0.707, p < 0.001). Since the p-value is far below the significance level of 0.05, we reject the null hypothesis and conclude that there is a statistically significant linear correlation between the two variables."

### Positivity Rate Paragraph
> "The mean test positivity rate was 8.84%, exceeding the WHO recommended threshold of 5%. However, the regression of deaths on positivity rate yielded an R² of only 0.003, indicating that positivity rate is not a meaningful predictor of daily deaths."
