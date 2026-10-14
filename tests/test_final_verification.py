
import sys
import math
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE))

from src.twin_engine import load_profiles
from src.simulator import simulate_profile, SCENARIOS

# ==========================================
# FINOVA AI - FINAL ENGINE VERIFICATION
# ==========================================

df = load_profiles()

HORIZONS = [12, 36, 120]

passed = 0
failed = []

print("=" * 55)
print("FINOVA AI - FINAL FINANCIAL VERIFICATION")
print("=" * 55)

for _, profile in df.iterrows():

    user_id = profile["user_id"]

    initial_cash = float(profile["current_balance"])
    initial_debt = float(profile["total_debt"])

    other_assets = (
        float(profile["total_assets"]) - initial_cash
    )

    goal_target = float(profile["target_amount"])

    is_emergency_goal = (
        profile["financial_goal"] == "Emergency Fund"
    )

    for months in HORIZONS:

        scenario_cash = {}

        for name, multiplier in SCENARIOS.items():

            try:

                history = simulate_profile(
                    profile,
                    months,
                    multiplier
                )

                assert len(history) == months

                previous_cash = initial_cash
                previous_debt = initial_debt

                for index, row in enumerate(history, start=1):

                    cash = row["projected_cash_position"]
                    debt = row["loan_balance"]
                    emergency = row["emergency_fund"]
                    goal_saved = row["goal_saved_so_far"]

                    assert row["month"] == index

                    # All financial values must be finite
                    for field in [
                        "projected_cash_position",
                        "monthly_cash_flow",
                        "loan_balance",
                        "emergency_fund",
                        "goal_saved_so_far",
                        "net_worth"
                    ]:
                        assert math.isfinite(row[field])

                    # Cash flow accounting
                    cash_change = cash - previous_cash

                    assert abs(
                        cash_change - row["monthly_cash_flow"]
                    ) <= 0.03

                    # Loan amortization accounting
                    expected_debt = max(
                        0.0,
                        previous_debt
                        + row["loan_interest"]
                        - row["loan_payment"]
                    )

                    assert abs(
                        debt - expected_debt
                    ) <= 0.03

                    # Loan must never become negative
                    assert debt >= -0.01

                    # Reserves must stay non-negative
                    assert emergency >= -0.01
                    assert goal_saved >= -0.01

                    # Goal cannot exceed target
                    assert goal_saved <= goal_target + 0.01

                    # Cash bucket validation
                    available_cash = max(0.0, cash)

                    if is_emergency_goal:
                        assert (
                            goal_saved <= emergency + 0.03
                        )
                    else:
                        assert (
                            emergency + goal_saved
                            <= available_cash + 0.03
                        )

                    assert emergency <= available_cash + 0.03

                    # Net worth consistency
                    expected_worth = (
                        other_assets + cash - debt
                    )

                    assert abs(
                        row["net_worth"] - expected_worth
                    ) <= 0.03

                    # Unfunded cash gap
                    expected_gap = max(0.0, -cash)

                    assert abs(
                        row["unfunded_cash_gap"] - expected_gap
                    ) <= 0.03

                    # Goal progress validation
                    expected_progress = (
                        goal_saved / goal_target * 100
                    )

                    assert abs(
                        row["goal_progress_pct"]
                        - expected_progress
                    ) <= 0.02

                    previous_cash = cash
                    previous_debt = debt

                scenario_cash[name] = history[-1][
                    "projected_cash_position"
                ]

                passed += 1

            except Exception as error:

                failed.append({
                    "user": user_id,
                    "months": months,
                    "scenario": name,
                    "error": str(error)
                })

        # Scenario cash ordering
        if len(scenario_cash) == len(SCENARIOS):

            try:
                assert (
                    scenario_cash["save_more"]
                    >= scenario_cash["baseline"] - 0.03
                )

                assert (
                    scenario_cash["baseline"]
                    >= scenario_cash["spend_more"] - 0.03
                )

            except AssertionError:
                failed.append({
                    "user": user_id,
                    "months": months,
                    "scenario": "comparison",
                    "error": "Scenario cash ordering failed"
                })

# ==========================================
# FINAL REPORT
# ==========================================

print("\n===== FINAL VERIFICATION RESULTS =====")

print("Total Users:", len(df))
print("Simulation Horizons:", HORIZONS)
print("Scenarios:", len(SCENARIOS))

print("\nPassed Executions:", passed)
print("Failed Checks:", len(failed))

if failed:

    print("\nFailure Details:")

    for item in failed[:20]:
        print(item)

    print("\nFINAL STATUS: FAILED")

else:

    print("\nAll financial verification checks passed!")
    print("FINAL STATUS: PASSED")

print("\nVerification Completed.")
