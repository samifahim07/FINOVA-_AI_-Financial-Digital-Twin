
import argparse
import json
from pathlib import Path

import pandas as pd

# ==========================================
# FINOVA AI - FINANCIAL DIGITAL TWIN
# DYNAMIC FINANCIAL SIMULATION ENGINE
# ==========================================

BASE = Path(__file__).resolve().parent.parent

DATA_PATH = (
    BASE / "data" / "raw" / "financial_profiles_v2.csv"
)

OUTPUT_DIR = BASE / "reports" / "simulations"

SCENARIOS = {
    "baseline": 1.00,
    "save_more": 0.90,
    "spend_more": 1.15
}


# ==========================================
# 1. SIMULATE A FINANCIAL PROFILE
# ==========================================

def simulate_profile(profile, months, living_multiplier):

    income = float(profile["monthly_income"])
    living = float(profile["living_expense"])

    standard_loan_payment = float(
        profile["monthly_loan_payment"]
    )

    annual_loan_rate = (
        float(profile["loan_apr_pct"]) / 100
    )

    loan_balance = float(profile["total_debt"])

    other_assets = (
        float(profile["total_assets"])
        - float(profile["current_balance"])
    )

    cash = float(profile["current_balance"])
    emergency = float(profile["emergency_fund"])
    goal_saved = float(profile["goal_saved_so_far"])

    # Cash not earmarked for either goal or emergency
    unassigned = cash - emergency - goal_saved

    goal_target = float(profile["target_amount"])
    goal_deadline = int(profile["target_months"])

    # Input safety checks
    if income <= 0 or goal_target <= 0 or goal_deadline <= 0:
        raise ValueError("Invalid income or goal values")

    components = [
        cash, emergency, goal_saved,
        unassigned, loan_balance, other_assets
    ]

    if min(components) < -0.01:
        raise ValueError("Invalid initial financial components")

    if goal_saved > goal_target + 0.01:
        raise ValueError("Goal savings exceed goal target")

    if loan_balance > 0 and standard_loan_payment <= 0:
        raise ValueError("Outstanding debt without loan payment")

    timeline = []

    # ======================================
    # 2. MONTHLY FINANCIAL EVOLUTION
    # ======================================

    for month in range(1, months + 1):

        # Loan amortization
        interest = loan_balance * annual_loan_rate / 12

        if loan_balance > 0:
            payment = min(
                standard_loan_payment,
                loan_balance + interest
            )
        else:
            payment = 0.0

        loan_balance = max(
            0.0,
            loan_balance + interest - payment
        )

        # Apply selected scenario
        living_cost = round(
            living * living_multiplier, 2
        )

        total_expense = living_cost + payment

        monthly_cash_flow = income - total_expense

        # Update projected cash
        cash += monthly_cash_flow

        # ==================================
        # 3. MANAGE CASH RESERVES
        # ==================================

        if monthly_cash_flow < 0:

            shortage = -monthly_cash_flow

            # Use unassigned cash first
            taken = min(unassigned, shortage)
            unassigned -= taken
            shortage -= taken

            # Then use goal savings
            taken = min(goal_saved, shortage)
            goal_saved -= taken
            shortage -= taken

            # Finally draw emergency reserves
            taken = min(emergency, shortage)
            emergency -= taken
            shortage -= taken

        else:

            # Clear negative cash positions before
            # allocating new money
            available = min(
                monthly_cash_flow,
                max(0.0, cash)
            )

            # First restore emergency coverage
            emergency_target = 3 * total_expense

            top_up = min(
                available,
                max(0.0, emergency_target - emergency)
            )

            emergency += top_up
            available -= top_up

            # Then contribute toward financial goal
            months_to_deadline = (
                goal_deadline - month + 1
            )

            if months_to_deadline > 0:

                goal_monthly_need = (
                    max(0.0, goal_target - goal_saved)
                    / months_to_deadline
                )

                goal_add = min(
                    available,
                    max(0.0, goal_target - goal_saved),
                    goal_monthly_need
                )

                goal_saved += goal_add
                available -= goal_add

            # Remaining surplus stays unassigned
            unassigned += available

        # ==================================
        # 4. ACCOUNTING VALIDATION
        # ==================================

        allocated_cash = (
            unassigned + emergency + goal_saved
        )

        if abs(
            allocated_cash - max(0.0, cash)
        ) > 0.02:
            raise AssertionError(
                "Cash bucket accounting is inconsistent"
            )

        # Negative cash is a funding shortfall,
        # not an automatically approved overdraft
        projected_assets = (
            other_assets + max(0.0, cash)
        )

        projected_liabilities = (
            loan_balance + max(0.0, -cash)
        )

        net_worth = (
            projected_assets - projected_liabilities
        )

        emergency_coverage = (
            emergency / total_expense
            if total_expense > 0 else 0
        )

        # ==================================
        # 5. FINANCIAL GOAL MONITORING
        # ==================================

        remaining_goal = max(
            0.0, goal_target - goal_saved
        )

        months_remaining = max(
            0, goal_deadline - month
        )

        if months_remaining > 0:

            required_next = (
                remaining_goal / months_remaining
            )

            goal_funding_gap = (
                required_next >
                max(0.0, monthly_cash_flow)
            )

        else:
            goal_funding_gap = remaining_goal > 0.01

        goal_progress = (
            goal_saved / goal_target * 100
        )

        # ==================================
        # 6. DYNAMIC RISK ASSESSMENT
        # ==================================

        risk_flags = {
            "negative_cash_flow":
                monthly_cash_flow < 0,

            "low_emergency_fund":
                emergency_coverage < 3,

            "high_debt_burden":
                payment / income > 0.20,

            "negative_net_worth":
                net_worth < 0,

            "goal_funding_gap":
                goal_funding_gap
        }

        risk_count = sum(risk_flags.values())

        if risk_count >= 3:
            risk_level = "HIGH"
        elif risk_count >= 1:
            risk_level = "MODERATE"
        else:
            risk_level = "LOW"

        # ==================================
        # 7. MONTHLY SNAPSHOT
        # ==================================

        timeline.append({
            "month": month,
            "income": round(income, 2),
            "living_expense": round(living_cost, 2),
            "loan_payment": round(payment, 2),
            "loan_interest": round(interest, 2),
            "monthly_cash_flow": round(
                monthly_cash_flow, 2
            ),
            "projected_cash_position": round(
                cash, 2
            ),
            "unfunded_cash_gap": round(
                max(0.0, -cash), 2
            ),
            "loan_balance": round(
                loan_balance, 2
            ),
            "emergency_fund": round(
                emergency, 2
            ),
            "goal_saved_so_far": round(
                goal_saved, 2
            ),
            "goal_progress_pct": round(
                goal_progress, 2
            ),
            "net_worth": round(net_worth, 2),
            "risk_level": risk_level,
            "risk_flags": risk_flags
        })

    return timeline


# ==========================================
# 8. EXECUTE SCENARIOS
# ==========================================

def main():

    parser = argparse.ArgumentParser(
        description="FINOVA AI Financial Twin Simulator"
    )

    parser.add_argument(
        "user_id",
        nargs="?",
        default="U0001"
    )

    parser.add_argument(
        "--months",
        type=int,
        default=12
    )

    args = parser.parse_args()

    if not 1 <= args.months <= 120:
        parser.error(
            "--months must be between 1 and 120"
        )

    # Load profile
    df = pd.read_csv(DATA_PATH)

    selected = df.loc[
        df["user_id"] == args.user_id
    ]

    if selected.empty:
        parser.error(
            f"Unknown user ID: {args.user_id}"
        )

    profile = selected.iloc[0]

    all_scenarios = []
    scenario_results = {}

    print(
        f"\nFINOVA AI | {args.user_id} | "
        f"{args.months}-Month Simulation"
    )

    # Run independent scenarios
    for name, multiplier in SCENARIOS.items():

        history = simulate_profile(
            profile,
            args.months,
            multiplier
        )

        scenario_results[name] = history

        # Flat structure for CSV output
        for record in history:

            flat_record = {
                "scenario": name,
                **{
                    k: v for k, v in record.items()
                    if k != "risk_flags"
                },
                **{
                    f"risk_{k}": v
                    for k, v in record["risk_flags"].items()
                }
            }

            all_scenarios.append(flat_record)

        final = history[-1]

        print(
            f"{name:12} | "
            f"Cash: {final['projected_cash_position']:,.2f} | "
            f"Debt: {final['loan_balance']:,.2f} | "
            f"Goal: {final['goal_progress_pct']:.2f}% | "
            f"Risk: {final['risk_level']}"
        )

    # ======================================
    # 9. SAVE SIMULATION OUTPUT
    # ======================================

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    filename = (
        f"simulation_{args.user_id}_{args.months}m"
    )

    csv_path = OUTPUT_DIR / f"{filename}.csv"
    json_path = OUTPUT_DIR / f"{filename}.json"

    pd.DataFrame(
        all_scenarios
    ).to_csv(csv_path, index=False)

    payload = {
        "user_id": args.user_id,
        "currency": str(profile["currency"]),
        "horizon_months": args.months,

        "assumptions": {
            "model": "rule_based_synthetic_simulation",
            "income_growth": 0,
            "inflation": 0,
            "investment_returns": 0,
            "living_expense_multipliers": SCENARIOS,
            "loan_model": "monthly_amortization",
            "emergency_fund_priority": True,
            "negative_cash_position":
                "unfunded_gap_not_bank_overdraft"
        },

        "scenarios": scenario_results
    }

    with open(
        json_path,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            payload,
            f,
            indent=4,
            ensure_ascii=False
        )

    print("\nSimulation Completed!")
    print("CSV:", csv_path)
    print("JSON:", json_path)


if __name__ == "__main__":
    main()
