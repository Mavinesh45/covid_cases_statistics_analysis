"""
Malaysia COVID-19 Data Analysis
University Statistics Project
=================================
Analyses cases, deaths, and testing data from the Malaysia Ministry of Health.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.linear_model import LinearRegression
from datetime import datetime
import os

# ─────────────────────────────────────────────
# 1. LOAD AND MERGE
# ─────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "DATASETS")

cases = pd.read_csv(os.path.join(DATA, "malaysia_covid_cases.csv"))
deaths = pd.read_csv(os.path.join(DATA, "malaysia_covid_deaths.csv"))
tests = pd.read_csv(os.path.join(DATA, "malaysia_covid_tests.csv"))

# Keep only the columns we need
cases = cases[["date", "cases_new"]]
deaths = deaths[["date", "deaths_new"]]
tests = tests[["date", "rtk-ag", "pcr"]]

# Merge on date
df = cases.merge(deaths, on="date", how="outer").merge(tests, on="date", how="outer")

print("=" * 60)
print("MALAYSIA COVID-19 ANALYSIS REPORT")
print("=" * 60)

# ─────────────────────────────────────────────
# 2. CLEAN THE DATA
# ─────────────────────────────────────────────
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date").reset_index(drop=True)

# Create total_tests = rtk-ag + pcr
df["total_tests"] = df["rtk-ag"] + df["pcr"]

# Drop rows missing key columns
before = len(df)
df = df.dropna(subset=["cases_new", "deaths_new", "total_tests"])
after = len(df)
print(f"\nRows before cleaning: {before}")
print(f"Rows after cleaning:  {after}")
print(f"Rows dropped:         {before - after}")

# ─────────────────────────────────────────────
# 3. DESCRIPTIVE STATISTICS
# ─────────────────────────────────────────────
print("\n" + "-" * 60)
print("DESCRIPTIVE STATISTICS")
print("-" * 60)

def describe(col, name):
    mode_vals = col.mode()
    mode = mode_vals.iloc[0] if not mode_vals.empty else np.nan
    return {
        "Variable": name,
        "Mean": round(col.mean(), 2),
        "Median": round(col.median(), 2),
        "Mode": round(mode, 2),
        "Std Dev": round(col.std(ddof=0), 2),
        "Variance": round(col.var(ddof=0), 2),
        "Min": round(col.min(), 2),
        "Max": round(col.max(), 2),
    }

rows = [
    describe(df["cases_new"], "New Cases"),
    describe(df["deaths_new"], "New Deaths"),
    describe(df["total_tests"], "Total Tests"),
]
desc_table = pd.DataFrame(rows).set_index("Variable")
print(desc_table.to_string())

# Save descriptive stats to CSV
desc_table.to_csv(os.path.join(BASE, "descriptive_stats.csv"))
print("\nDescriptive stats saved to descriptive_stats.csv")

# ─────────────────────────────────────────────
# 4. DATA VISUALIZATIONS
# ─────────────────────────────────────────────

# 4a. Line chart – daily new cases
plt.figure(figsize=(12, 5))
plt.plot(df["date"], df["cases_new"], color="crimson", linewidth=0.8)
plt.title("Daily New COVID-19 Cases in Malaysia", fontsize=14)
plt.xlabel("Date")
plt.ylabel("New Cases")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(BASE, "daily_new_cases_line.png"), dpi=150)
plt.close()
print("\nSaved: daily_new_cases_line.png")

# 4b. Scatter plot – total tests vs new cases
plt.figure(figsize=(8, 6))
plt.scatter(df["total_tests"], df["cases_new"], alpha=0.4, s=10, color="steelblue")
plt.title("Total Tests vs New Cases", fontsize=14)
plt.xlabel("Total Tests (RTK-AG + PCR)")
plt.ylabel("New Cases")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(BASE, "tests_vs_cases_scatter.png"), dpi=150)
plt.close()
print("Saved: tests_vs_cases_scatter.png")

# 4c. Bar chart – monthly sum of cases and deaths
df["month"] = df["date"].dt.to_period("M").astype(str)
monthly = df.groupby("month").agg(
    cases_monthly=("cases_new", "sum"),
    deaths_monthly=("deaths_new", "sum"),
).reset_index()

x = np.arange(len(monthly))
width = 0.4

fig, ax1 = plt.subplots(figsize=(14, 5))
ax1.bar(x - width / 2, monthly["cases_monthly"], width, label="Cases", color="crimson", alpha=0.7)
ax1.set_ylabel("Cases", color="crimson")
ax1.tick_params(axis="y", labelcolor="crimson")

ax2 = ax1.twinx()
ax2.bar(x + width / 2, monthly["deaths_monthly"], width, label="Deaths", color="navy", alpha=0.7)
ax2.set_ylabel("Deaths", color="navy")
ax2.tick_params(axis="y", labelcolor="navy")

# Show only every 6th month label to avoid clutter
step = max(1, len(monthly) // 12)
tick_positions = x[::step]
tick_labels = monthly["month"].iloc[::step].values
ax1.set_xticks(tick_positions)
ax1.set_xticklabels(tick_labels, rotation=45, ha="right")
fig.suptitle("Monthly COVID-19 Cases and Deaths in Malaysia", fontsize=14)
fig.tight_layout()
fig.savefig(os.path.join(BASE, "monthly_cases_deaths_bar.png"), dpi=150)
plt.close()
print("Saved: monthly_cases_deaths_bar.png")

# ─────────────────────────────────────────────
# 5. INFERENTIAL STATISTICS
# ─────────────────────────────────────────────
print("\n" + "-" * 60)
print("INFERENTIAL STATISTICS")
print("-" * 60)

# 5a. Linear regression: deaths_new ~ cases_new
X = df[["cases_new"]].values
y = df["deaths_new"].values
reg = LinearRegression()
reg.fit(X, y)
y_pred = reg.predict(X)

# R-squared manually (same as reg.score(X, y))
ss_res = np.sum((y - y_pred) ** 2)
ss_tot = np.sum((y - np.mean(y)) ** 2)
r_sq = 1 - ss_res / ss_tot

print(f"\nRegression: deaths_new ~ cases_new")
print(f"  Coefficient:  {reg.coef_[0]:.6f}")
print(f"  Intercept:    {reg.intercept_:.6f}")
print(f"  R-squared:    {r_sq:.6f}")

# 5b. Pearson correlation
corr, p_value = stats.pearsonr(df["cases_new"], df["deaths_new"])
print(f"\nPearson correlation (cases_new vs deaths_new):")
print(f"  r         = {corr:.6f}")
print(f"  p-value   = {p_value:.6e}")
print(f"  alpha     = 0.05")

if p_value < 0.05:
    print(f"  Conclusion: REJECT H0 — Significant linear relationship exists.")
else:
    print(f"  Conclusion: Fail to reject H0 — No significant linear relationship.")

# ─────────────────────────────────────────────
# 6. BONUS – POSITIVITY RATE
# ─────────────────────────────────────────────
print("\n" + "-" * 60)
print("BONUS: TEST POSITIVITY RATE ANALYSIS")
print("-" * 60)

df["positivity_rate"] = (df["cases_new"] / df["total_tests"]) * 100

# Regression: deaths_new ~ positivity_rate
X2 = df[["positivity_rate"]].values
reg2 = LinearRegression()
reg2.fit(X2, y)
y_pred2 = reg2.predict(X2)
ss_res2 = np.sum((y - y_pred2) ** 2)
r_sq2 = 1 - ss_res2 / ss_tot

print(f"  Regression: deaths_new ~ positivity_rate")
print(f"  Coefficient:  {reg2.coef_[0]:.6f}")
print(f"  Intercept:    {reg2.intercept_:.6f}")
print(f"  R-squared:    {r_sq2:.6f}")
print(f"\n  Mean positivity rate: {df['positivity_rate'].mean():.2f}%")

print("\n" + "=" * 60)
print("ANALYSIS COMPLETE")
print("=" * 60)
