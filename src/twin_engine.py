
import json
import sys
from pathlib import Path

import pandas as pd

# ==========================================
# FINOVA AI - FINANCIAL DIGITAL TWIN ENGINE
# VERSION 1: FINANCIAL STATE ENGINE
# ==========================================

BASE = Path(__file__).resolve().parent.parent

DATA_PATH = BASE / "data" / "raw" / "financial_profiles_v2.csv"
REPORT_DIR = BASE / "reports"

REPORT_DIR.mkdir(parents=True, exist_ok=True)


# ==========================================
# 1. LOAD FINANCIAL PROFILES
# ==========================================

def load_profiles():
    df = pd.read_csv(DATA_PATH)

    if df["user_id"].duplicated().any():
        raise ValueError("Duplicate user IDs detected")

    if df.isna().any().any():
        raise ValueError("Missing profile values detected")

    if not (
        df["monthly_expense"]
        == df["living_expense"] + df["monthly_loan_payment"]
    ).all():
        raise ValueError("Inconsistent monthly expenses")

    if not (
        df["monthly_cash_flow"]
        == df["monthly_income"] - df["monthly_expense"]
    ).all():
        raise ValueError("Inconsistent monthly cash flow")

    return df


# ==========================================
# 2. FINANCIAL TWIN ENGINE
# ==========================================

def build_financial_twin(profile):

    income = float(profile["monthly_income"])
    expense = float(profile["monthly_expense"])
    cash_flow = float(profile["monthly_cash_flow"])

    balance = float(profile["current_balance"])
    emergency_fund = float(profile["emergency_fund"])

    assets = float(profile["total_assets"])
    debt = float(profile["total_debt"])
    loan_payment = float(profile["monthly_loan_payment"])

    # Financial ratios
    savings_rate = (cash_flow / income) * 100
    expense_ratio = (expense / income) * 100
    debt_service_ratio = (loan_payment / income) * 100

    emergency_months = (
        emergency_fund / expense if expense > 0 else 0
    )

    net_worth = assets - debt

    debt_asset_ratio = (
        (debt / assets) * 100 if assets > 0 else 0
    )

    # ======================================
    # 3. FINANCIAL GOAL ANALYSIS
    # ======================================

    goal = str(profile["financial_goal"])
    target_amount = float(profile["target_amount"])
    goal_saved = float(profile["goal_saved_so_far"])
    target_months = int(profile["target_months"])

    remaining_goal = max(
        0, target_amount - goal_saved
    )

    monthly_goal_requirement = (
        remaining_goal / target_months
    )

    available_surplus = max(0, cash_flow)

    goal_feasible = (
        monthly_goal_requirement <= available_surplus
    )

    goal_progress = (
        (goal_saved / target_amount) * 100
        if target_amount > 0 else 100
    )

    # ======================================
    # 4. FINANCIAL RISK DETECTION
    # ======================================

    risk_flags = {
        "negative_cash_flow": cash_flow < 0,
        "low_emergency_fund": emergency_months < 3,
        "high_debt_burden": debt_service_ratio > 20,
        "negative_net_worth": net_worth < 0,
        "goal_funding_gap": not goal_feasible
    }

    risk_count = sum(risk_flags.values())

    if risk_count >= 3:
        risk_level = "HIGH"
    elif risk_count >= 1:
        risk_level = "MODERATE"
    else:
        risk_level = "LOW"

    # Estimated liquidity runway if monthly
    # cash flow stays negative
    cash_runway = (
        round(balance / abs(cash_flow), 2)
        if cash_flow < 0 else None
    )

    # ======================================
    # 5. BUILD DIGITAL TWIN SNAPSHOT
    # ======================================

    twin = {
        "user_id": str(profile["user_id"]),

        "persona": str(profile["persona"]),

        "currency": str(profile["currency"]),

        "financial_state": {
            "monthly_income": income,
            "monthly_expense": expense,
            "monthly_cash_flow": cash_flow,
            "current_balance": balance,
            "emergency_fund": emergency_fund,
            "total_assets": assets,
            "total_debt": debt,
            "net_worth": net_worth
        },

        "financial_ratios": {
            "savings_rate_pct": round(savings_rate, 2),
            "expense_ratio_pct": round(expense_ratio, 2),
            "debt_service_ratio_pct": round(
                debt_service_ratio, 2
            ),
            "emergency_coverage_months": round(
                emergency_months, 2
            ),
            "debt_to_asset_ratio_pct": round(
                debt_asset_ratio, 2
            )
        },

        "financial_goal": {
            "goal": goal,
            "target_amount": target_amount,
            "saved_so_far": goal_saved,
            "remaining_amount": remaining_goal,
            "target_months": target_months,
            "required_monthly_savings": round(
                monthly_goal_requirement, 2
            ),
            "goal_progress_pct": round(
                goal_progress, 2
            ),
            "feasible_from_current_surplus": goal_feasible
        },

        "risk_assessment": {
            "risk_level": risk_level,
            "total_risk_flags": risk_count,
            "risk_flags": risk_flags,
            "cash_runway_months": cash_runway
        },

        "metadata": {
            "engine_version": "1.0",
            "profile_source": str(profile["data_source"]),
            "risk_method": "rule_based_heuristics",
            "snapshot_type": "synthetic_demo"
        }
    }

    return twin


# ==========================================
# 6. RUN SINGLE USER DIGITAL TWIN
# ==========================================

def run_twin(user_id):

    df = load_profiles()

    selected = df[df["user_id"] == user_id]

    if selected.empty:
        raise ValueError(f"User {user_id} not found")

    profile = selected.iloc[0]

    twin = build_financial_twin(profile)

    # Save output
    output_file = REPORT_DIR / f"twin_{user_id}.json"

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(twin, f, indent=4, ensure_ascii=False)

    print("\n===== FINOVA AI FINANCIAL DIGITAL TWIN =====")

    print(json.dumps(twin, indent=4, ensure_ascii=False))

    print("\nTwin Saved At:")
    print(output_file)

    return twin


# ==========================================
# EXECUTION
# ==========================================

if __name__ == "__main__":

    user_id = sys.argv[1] if len(sys.argv) > 1 else "U0001"

    run_twin(user_id)
