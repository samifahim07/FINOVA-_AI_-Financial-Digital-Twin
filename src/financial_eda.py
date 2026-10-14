
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# ==========================================
# STEP 3: FINANCIAL DIGITAL TWIN - EDA
# ==========================================

BASE = Path(__file__).resolve().parent.parent

DATA_PATH = BASE / "data" / "raw" / "financial_profiles.csv"
PROCESSED_DIR = BASE / "data" / "processed"
REPORT_DIR = BASE / "reports"
FIGURE_DIR = REPORT_DIR / "figures"

for folder in [PROCESSED_DIR, REPORT_DIR, FIGURE_DIR]:
    folder.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA_PATH)

print("=" * 55)
print("FINOVA AI - FINANCIAL DIGITAL TWIN ANALYSIS")
print("=" * 55)

print("\nDataset Shape:", df.shape)

# ==========================================
# 1. FEATURE ENGINEERING
# ==========================================

# Savings rate includes negative cash flow
df["savings_rate_pct"] = (
    df["monthly_cash_flow"] / df["monthly_income"] * 100
)

# Expense-to-income ratio
df["expense_ratio_pct"] = (
    df["monthly_expense"] / df["monthly_income"] * 100
)

# Debt service ratio
df["debt_service_ratio_pct"] = (
    df["monthly_loan_payment"] / df["monthly_income"] * 100
)

# Emergency fund coverage in months
df["emergency_coverage_months"] = (
    df["emergency_fund"] / df["monthly_expense"]
)

# Debt-to-asset ratio
df["debt_to_asset_ratio_pct"] = np.where(
    df["total_assets"] > 0,
    df["total_debt"] / df["total_assets"] * 100,
    np.nan
)

# Required monthly goal contribution
df["goal_monthly_requirement"] = (
    df["target_amount"] / df["target_months"]
)

# ==========================================
# 2. FINANCIAL RISK FLAGS
# ==========================================

# Negative monthly cash flow
df["negative_cash_flow"] = (
    df["monthly_cash_flow"] < 0
)

# Emergency savings cover less than 3 months
df["low_emergency_fund"] = (
    df["emergency_coverage_months"] < 3
)

# Loan payments exceed 20% of income
df["high_debt_burden"] = (
    df["debt_service_ratio_pct"] > 20
)

# Total liabilities exceed total assets
df["negative_net_worth"] = (
    df["net_worth"] < 0
)

# Goal requires more than available monthly surplus
df["goal_unaffordable"] = (
    df["goal_monthly_requirement"] >
    df["monthly_cash_flow"].clip(lower=0)
)

risk_columns = [
    "negative_cash_flow",
    "low_emergency_fund",
    "high_debt_burden",
    "negative_net_worth",
    "goal_unaffordable"
]

df["risk_flag_count"] = df[risk_columns].sum(axis=1)

# ==========================================
# 3. FINANCIAL STATISTICS
# ==========================================

print("\n===== INCOME & EXPENSE ANALYSIS =====")

print("Average Income:",
      round(df["monthly_income"].mean(), 2))

print("Median Income:",
      round(df["monthly_income"].median(), 2))

print("Average Expense:",
      round(df["monthly_expense"].mean(), 2))

print("Average Cash Flow:",
      round(df["monthly_cash_flow"].mean(), 2))

print("Median Savings Rate (%):",
      round(df["savings_rate_pct"].median(), 2))

print("\n===== FINANCIAL RISK ANALYSIS =====")

for col in risk_columns:
    count = int(df[col].sum())
    percentage = df[col].mean() * 100

    print(
        f"{col}: {count} users "
        f"({percentage:.2f}%)"
    )

print("\n===== FINANCIAL HEALTH =====")

print("Average Net Worth:",
      round(df["net_worth"].mean(), 2))

print("Median Emergency Coverage (months):",
      round(df["emergency_coverage_months"].median(), 2))

print("Users With Loans:",
      int((df["total_debt"] > 0).sum()))

print("\n===== FINANCIAL GOALS =====")
print(df["financial_goal"].value_counts())

# ==========================================
# 4. SAVE ENRICHED DATASET
# ==========================================

processed_path = (
    PROCESSED_DIR / "financial_profiles_enriched.csv"
)

df.to_csv(processed_path, index=False)

# ==========================================
# 5. SAVE SUMMARY REPORT
# ==========================================

summary = pd.DataFrame({
    "metric": [
        "total_users",
        "average_income",
        "average_expense",
        "average_cash_flow",
        "median_savings_rate_pct",
        "median_emergency_months",
        "negative_cash_flow_users",
        "low_emergency_fund_users",
        "high_debt_burden_users",
        "negative_net_worth_users",
        "goal_unaffordable_users"
    ],
    "value": [
        len(df),
        df["monthly_income"].mean(),
        df["monthly_expense"].mean(),
        df["monthly_cash_flow"].mean(),
        df["savings_rate_pct"].median(),
        df["emergency_coverage_months"].median(),
        df["negative_cash_flow"].sum(),
        df["low_emergency_fund"].sum(),
        df["high_debt_burden"].sum(),
        df["negative_net_worth"].sum(),
        df["goal_unaffordable"].sum()
    ]
})

summary.to_csv(
    REPORT_DIR / "financial_eda_summary.csv",
    index=False
)

# ==========================================
# 6. DATA VISUALIZATION
# ==========================================

def save_histogram(column, title, xlabel, filename):
    plt.figure(figsize=(9, 5))

    plt.hist(
        df[column].dropna(),
        bins=25,
        edgecolor="black",
        alpha=0.8
    )

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel("Number of Users")
    plt.tight_layout()

    plt.savefig(
        FIGURE_DIR / filename,
        dpi=200,
        bbox_inches="tight"
    )

    plt.close()

save_histogram(
    "monthly_income",
    "Monthly Income Distribution",
    "Monthly Income (BDT)",
    "income_distribution.png"
)

save_histogram(
    "monthly_expense",
    "Monthly Expense Distribution",
    "Monthly Expense (BDT)",
    "expense_distribution.png"
)

save_histogram(
    "savings_rate_pct",
    "Monthly Savings Rate Distribution",
    "Cash Flow / Income (%)",
    "savings_distribution.png"
)

save_histogram(
    "emergency_coverage_months",
    "Emergency Fund Coverage",
    "Months of Expense Coverage",
    "emergency_fund.png"
)

# ==========================================
# 7. RISK FLAG VISUALIZATION
# ==========================================

risk_counts = df[risk_columns].sum()

plt.figure(figsize=(10, 5))

plt.bar(
    risk_counts.index,
    risk_counts.values
)

plt.title("Financial Risk Flag Distribution")
plt.ylabel("Number of Users")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()

plt.savefig(
    FIGURE_DIR / "financial_risk_flags.png",
    dpi=200,
    bbox_inches="tight"
)

plt.close()

# ==========================================
# FINAL OUTPUT
# ==========================================

print("\n===== ANALYSIS COMPLETED =====")

print("Processed Dataset:")
print(processed_path)

print("\nSummary Report:")
print(REPORT_DIR / "financial_eda_summary.csv")

print("\nVisualizations:")
for file in sorted(FIGURE_DIR.glob("*.png")):
    print("-", file.name)

print("\nFinancial EDA completed successfully!")
