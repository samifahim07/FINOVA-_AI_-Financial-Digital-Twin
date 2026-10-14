
from pathlib import Path
import numpy as np
import pandas as pd


# FINOVA AI - FINANCIAL PROFILE GENERATOR V2


rng = np.random.default_rng(42)

N_USERS = 500

# Financial personas
personas = {
    "early_career": {
        "income": (25000, 70000),
        "living": (0.60, 0.92),
        "loan_probability": 0.30,
        "asset_months": (0, 5)
    },
    "working_professional": {
        "income": (55000, 135000),
        "living": (0.48, 0.84),
        "loan_probability": 0.55,
        "asset_months": (1, 14)
    },
    "family_household": {
        "income": (60000, 170000),
        "living": (0.62, 0.95),
        "loan_probability": 0.70,
        "asset_months": (2, 28)
    },
    "high_income": {
        "income": (130000, 250000),
        "living": (0.40, 0.78),
        "loan_probability": 0.60,
        "asset_months": (5, 40)
    }
}

# Possible financial goals
available_goals = {
    "early_career": [
        "Emergency Fund", "Education",
        "Travel", "Start Business"
    ],
    "working_professional": [
        "Emergency Fund", "Buy Car",
        "Buy House", "Education", "Travel"
    ],
    "family_household": [
        "Emergency Fund", "Buy Car",
        "Buy House", "Education", "Start Business"
    ],
    "high_income": [
        "Buy House", "Start Business",
        "Buy Car", "Travel", "Education"
    ]
}

goal_ranges = {
    "Education": (150000, 800000),
    "Travel": (60000, 250000),
    "Buy Car": (700000, 2500000),
    "Buy House": (3000000, 12000000),
    "Start Business": (400000, 3000000)
}

goal_timelines = {
    "Emergency Fund": [6, 12, 18, 24],
    "Education": [12, 24, 36, 48],
    "Travel": [6, 12, 18],
    "Buy Car": [24, 36, 60],
    "Buy House": [60, 84, 120],
    "Start Business": [24, 36, 60]
}

rows = []

# GENERATE FINANCIAL PROFILES


for i in range(1, N_USERS + 1):

    persona = str(
        rng.choice(
            list(personas),
            p=[0.25, 0.38, 0.27, 0.10]
        )
    )

    conf = personas[persona]

    # Income based on financial persona
    income = int(
        rng.integers(
            conf["income"][0] // 1000,
            conf["income"][1] // 1000 + 1
        )
    ) * 1000

    living_expense = round(
        income * rng.uniform(*conf["living"])
    )

    # Loan generation
    has_loan = bool(
        rng.random() < conf["loan_probability"]
    )

    if has_loan:

        loan_payment = round(
            income * rng.uniform(0.08, 0.35)
        )

        loan_apr_pct = round(
            float(rng.uniform(7, 17)), 2
        )

        loan_remaining_months = int(
            rng.integers(8, 73)
        )

        monthly_rate = loan_apr_pct / 1200

        # Estimated outstanding principal
        total_debt = round(
            loan_payment
            * (1 - (1 + monthly_rate)
               ** (-loan_remaining_months))
            / monthly_rate
        )

    else:
        loan_payment = 0
        loan_apr_pct = 0
        loan_remaining_months = 0
        total_debt = 0

    # Cash flow calculations
    monthly_expense = living_expense + loan_payment

    monthly_cash_flow = income - monthly_expense

    monthly_savings = max(monthly_cash_flow, 0)

    # Financial assets
    current_balance = round(
        income * rng.uniform(0.05, 7.0)
    )

    emergency_fund = round(
        current_balance * rng.uniform(0.04, 0.85)
    )

    other_assets = round(
        income * rng.uniform(*conf["asset_months"])
    )

    total_assets = current_balance + other_assets

    net_worth = total_assets - total_debt

    # Goals based on persona
    goal_name = str(
        rng.choice(available_goals[persona])
    )

    if goal_name == "Emergency Fund":

        target_amount = round(
            monthly_expense * rng.uniform(3, 6)
        )

        goal_saved = min(
            target_amount, emergency_fund
        )

    else:

        low, high = goal_ranges[goal_name]

        target_amount = int(
            rng.integers(
                low // 1000,
                high // 1000 + 1
            )
        ) * 1000

        available_for_goal = (
            current_balance - emergency_fund
        )

        goal_saved = min(
            target_amount,
            round(
                available_for_goal
                * rng.uniform(0, 0.55)
            )
        )

    target_months = int(
        rng.choice(goal_timelines[goal_name])
    )

    rows.append({
        "user_id": f"U{i:04d}",
        "persona": persona,
        "currency": "BDT",
        "monthly_income": income,
        "living_expense": living_expense,
        "monthly_loan_payment": loan_payment,
        "monthly_expense": monthly_expense,
        "monthly_cash_flow": monthly_cash_flow,
        "monthly_savings": monthly_savings,
        "current_balance": current_balance,
        "emergency_fund": emergency_fund,
        "total_debt": total_debt,
        "loan_apr_pct": loan_apr_pct,
        "loan_remaining_months": loan_remaining_months,
        "total_assets": total_assets,
        "net_worth": net_worth,
        "financial_goal": goal_name,
        "target_amount": target_amount,
        "goal_saved_so_far": goal_saved,
        "target_months": target_months,
        "data_source": "synthetic_v2"
    })


# DATA VALIDATION


df = pd.DataFrame(rows)

assert df["user_id"].is_unique

assert (
    df["monthly_expense"]
    == df["living_expense"] + df["monthly_loan_payment"]
).all()

assert (
    df["monthly_cash_flow"]
    == df["monthly_income"] - df["monthly_expense"]
).all()

assert (
    df["emergency_fund"] <= df["current_balance"]
).all()

assert (
    (df["goal_saved_so_far"] >= 0)
    & (df["goal_saved_so_far"] <= df["target_amount"])
).all()


# SAVE DATASET


BASE = Path(__file__).resolve().parent.parent

OUTPUT_DIR = BASE / "data" / "raw"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "financial_profiles_v2.csv"

df.to_csv(OUTPUT_FILE, index=False)

# ==========================================
# REPORT
# ==========================================

print("\n===== FINANCIAL PROFILES V2 =====")

print("Dataset Shape:", df.shape)

print("\nFinancial Personas:")
print(df["persona"].value_counts())

print("\nFinancial Risk Indicators:")

high_debt = (
    df["monthly_loan_payment"]
    / df["monthly_income"] > 0.20
).sum()

negative_cash_flow = (
    df["monthly_cash_flow"] < 0
).sum()

negative_net_worth = (
    df["net_worth"] < 0
).sum()

print("High Debt Burden:", high_debt)
print("Negative Cash Flow:", negative_cash_flow)
print("Negative Net Worth:", negative_net_worth)

print("\nMissing Values:", df.isna().sum().sum())
print("Duplicate IDs:", df["user_id"].duplicated().sum())

print("\nDataset Saved:")
print(OUTPUT_FILE)

print("\nGeneration Completed Successfully!")
