
import sys
from pathlib import Path
import math

BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE))

from src.twin_engine import (
    load_profiles,
    build_financial_twin
)
from src.simulator import (
    simulate_profile,
    SCENARIOS
)

print("=" * 55)
print("FINOVA AI - FINANCIAL DIGITAL TWIN ENGINE AUDIT")
print("=" * 55)

df = load_profiles()

passed = 0
failed = []

for _, profile in df.iterrows():

    user_id = profile["user_id"]

    try:
        # Test Financial Twin snapshot
        twin = build_financial_twin(profile)

        assert twin["user_id"] == user_id

        # Test all 3 financial scenarios
        for scenario, multiplier in SCENARIOS.items():

            timeline = simulate_profile(
                profile,
                months=12,
                living_multiplier=multiplier
            )

            assert len(timeline) == 12

            for month in timeline:

                assert math.isfinite(
                    month["projected_cash_position"]
                )

                assert math.isfinite(
                    month["net_worth"]
                )

                assert month["loan_balance"] >= -0.01

                assert month["emergency_fund"] >= -0.01

                assert (
                    0 <= month["goal_progress_pct"] <= 100.01
                )

                assert (
                    month["unfunded_cash_gap"] >= -0.01
                )

        passed += 1

    except Exception as error:

        failed.append({
            "user_id": user_id,
            "error": str(error)
        })

print("\n===== AUDIT RESULTS =====")

print("Total Users:", len(df))
print("Passed:", passed)
print("Failed:", len(failed))

if failed:
    print("\nFailed Profiles:")

    for item in failed[:20]:
        print(item)

else:
    print("\nAll basic engine checks passed!")

print("\nAudit Completed.")
