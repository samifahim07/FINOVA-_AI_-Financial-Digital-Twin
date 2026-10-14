
import pandas as pd
import random
from pathlib import Path

random.seed(42)

profiles = []

financial_goals = [
    ("Emergency Fund", 200000),
    ("Buy Car", 800000),
    ("Buy House", 3000000),
    ("Education", 500000),
    ("Travel", 150000),
    ("Start Business", 1000000)
]

# Generate 500 financial profiles

for i in range(1, 501):

    user_id = "U" + str(i).zfill(4)

    # Monthly income
    income = random.randint(25, 180) * 1000

    # Monthly living expense
    living_expense = round(
        income * random.uniform(0.45, 1.00)
    )

    # Loan information
    has_loan = random.choice([True, False])

    if has_loan:
        loan_payment = round(
            income * random.uniform(0.05, 0.20)
        )
        total_debt = loan_payment * random.randint(8, 48)
    else:
        loan_payment = 0
        total_debt = 0

    # Monthly financial calculations
    monthly_expense = living_expense + loan_payment

    monthly_cash_flow = income - monthly_expense

    monthly_savings = max(monthly_cash_flow, 0)

    # Current financial condition
    current_balance = round(
        income * random.uniform(0.2, 10)
    )

    emergency_fund = round(
        current_balance * random.uniform(0.10, 0.70)
    )

    other_assets = round(
        income * random.uniform(0, 24)
    )

    total_assets = current_balance + other_assets

    net_worth = total_assets - total_debt

    # Financial goals
    goal_name, target_amount = random.choice(financial_goals)

    target_months = random.choice([12, 24, 36, 48, 60])

    # Store profile
    profiles.append({
        "user_id": user_id,
        "monthly_income": income,
        "living_expense": living_expense,
        "monthly_loan_payment": loan_payment,
        "monthly_expense": monthly_expense,
        "monthly_cash_flow": monthly_cash_flow,
        "monthly_savings": monthly_savings,
        "current_balance": current_balance,
        "emergency_fund": emergency_fund,
        "total_debt": total_debt,
        "total_assets": total_assets,
        "net_worth": net_worth,
        "financial_goal": goal_name,
        "target_amount": target_amount,
        "target_months": target_months,
        "data_source": "synthetic"
    })

# Convert to DataFrame
df = pd.DataFrame(profiles)

# Save dataset
project_folder = Path(__file__).resolve().parent.parent

output_folder = project_folder / "data" / "raw"
output_folder.mkdir(parents=True, exist_ok=True)

output_file = output_folder / "financial_profiles.csv"

df.to_csv(output_file, index=False)

print("Financial Profiles Generated Successfully!")

print("\nDataset Shape:")
print(df.shape)

print("\nFirst 5 Records:")
print(df.head())

print("\nMissing Values:")
print(df.isnull().sum().sum())

print("\nDuplicate User IDs:")
print(df["user_id"].duplicated().sum())

print("\nDataset Saved At:")
print(output_file)
