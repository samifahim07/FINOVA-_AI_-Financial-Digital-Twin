
import pandas as pd
from pathlib import Path

# Load dataset
project_folder = Path(__file__).resolve().parent.parent

file_path = project_folder / "data" / "raw" / "financial_profiles.csv"

df = pd.read_csv(file_path)

print("===== FINANCIAL DATA VALIDATION =====")

# 1. Missing values
print("\nMissing Values:")
print(df.isnull().sum().sum())

# 2. Duplicate user IDs
print("\nDuplicate User IDs:")
print(df["user_id"].duplicated().sum())

# 3. Income validation
invalid_income = (df["monthly_income"] <= 0).sum()

print("\nInvalid Income:", invalid_income)

# 4. Expense validation
invalid_expense = (
    df["monthly_expense"] !=
    df["living_expense"] + df["monthly_loan_payment"]
).sum()

print("Invalid Expense:", invalid_expense)

# 5. Cash flow validation
invalid_cash_flow = (
    df["monthly_cash_flow"] !=
    df["monthly_income"] - df["monthly_expense"]
).sum()

print("Invalid Cash Flow:", invalid_cash_flow)

# 6. Savings validation
expected_savings = df["monthly_cash_flow"].clip(lower=0)

invalid_savings = (
    df["monthly_savings"] != expected_savings
).sum()

print("Invalid Savings:", invalid_savings)

# 7. Debt validation
invalid_debt = (
    (df["total_debt"] < 0) |
    (df["monthly_loan_payment"] < 0) |
    ((df["total_debt"] == 0) & (df["monthly_loan_payment"] > 0)) |
    ((df["total_debt"] > 0) & (df["monthly_loan_payment"] == 0))
).sum()

print("Invalid Debt:", invalid_debt)

# 8. Asset validation
invalid_assets = (
    (df["total_assets"] < df["current_balance"]) |
    (df["current_balance"] < 0) |
    (df["emergency_fund"] < 0) |
    (df["emergency_fund"] > df["current_balance"])
).sum()

print("Invalid Assets:", invalid_assets)

# 9. Net worth validation
invalid_net_worth = (
    df["net_worth"] !=
    df["total_assets"] - df["total_debt"]
).sum()

print("Invalid Net Worth:", invalid_net_worth)

# Final validation
total_errors = (
    df.isnull().sum().sum()
    + df["user_id"].duplicated().sum()
    + invalid_income
    + invalid_expense
    + invalid_cash_flow
    + invalid_savings
    + invalid_debt
    + invalid_assets
    + invalid_net_worth
)

print("\n===== FINAL RESULT =====")

if total_errors == 0:
    print("All financial consistency checks passed!")
else:
    print("Total Validation Errors:", total_errors)
