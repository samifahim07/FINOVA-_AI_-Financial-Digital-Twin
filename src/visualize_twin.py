
import argparse
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ==========================================
# FINOVA AI - FINANCIAL DIGITAL TWIN
# INTERACTIVE FINANCIAL TIMELINE
# ==========================================

BASE = Path(__file__).resolve().parent.parent

DATA_PATH = (
    BASE / "data" / "raw" / "financial_profiles_v2.csv"
)

SIM_DIR = BASE / "reports" / "simulations"
OUTPUT_DIR = BASE / "reports" / "visualizations"

SCENARIOS = {
    "baseline": {
        "label": "Baseline",
        "color": "#2DD4BF"
    },
    "save_more": {
        "label": "Save More",
        "color": "#A78BFA"
    },
    "spend_more": {
        "label": "Spend More",
        "color": "#FB7185"
    }
}


# ==========================================
# 1. LOAD PROFILE AND SIMULATION
# ==========================================

def load_data(user_id, months):

    profiles = pd.read_csv(DATA_PATH)

    selected = profiles.loc[
        profiles["user_id"] == user_id
    ]

    if selected.empty:
        raise ValueError(
            f"User not found: {user_id}"
        )

    csv_path = (
        SIM_DIR
        / f"simulation_{user_id}_{months}m.csv"
    )

    if not csv_path.exists():
        raise FileNotFoundError(
            f"Simulation not found: {csv_path}\n"
            "Run simulator.py first."
        )

    simulation = pd.read_csv(csv_path)

    required = {
        "scenario", "month",
        "projected_cash_position",
        "loan_balance",
        "goal_progress_pct",
        "net_worth",
        "risk_level"
    }

    missing = required - set(simulation.columns)

    if missing:
        raise ValueError(
            f"Missing simulation columns: {missing}"
        )

    for scenario in SCENARIOS:

        subset = simulation[
            simulation["scenario"] == scenario
        ]

        expected_months = list(range(1, months + 1))
        actual_months = sorted(
            subset["month"].tolist()
        )

        if actual_months != expected_months:
            raise ValueError(
                f"Incomplete timeline: {scenario}"
            )

    return selected.iloc[0], simulation


# ==========================================
# 2. CREATE INTERACTIVE DASHBOARD
# ==========================================

def create_visualization(user_id, months):

    profile, df = load_data(user_id, months)

    currency = str(profile["currency"])

    initial_cash = float(
        profile["current_balance"]
    )

    initial_debt = float(
        profile["total_debt"]
    )

    initial_net_worth = float(
        profile["net_worth"]
    )

    initial_goal_progress = (
        float(profile["goal_saved_so_far"])
        / float(profile["target_amount"])
        * 100
    )

    fig = make_subplots(
        rows=2,
        cols=2,
        subplot_titles=[
            "Projected Cash Position",
            "Financial Goal Progress",
            "Outstanding Loan Balance",
            "Projected Net Worth"
        ],
        horizontal_spacing=0.12,
        vertical_spacing=0.17
    )

    summary_rows = []

    # ======================================
    # 3. PLOT ALL SCENARIOS
    # ======================================

    for scenario, config in SCENARIOS.items():

        subset = (
            df[df["scenario"] == scenario]
            .sort_values("month")
        )

        x = [0] + subset["month"].tolist()

        cash_values = (
            [initial_cash]
            + subset["projected_cash_position"].tolist()
        )

        goal_values = (
            [initial_goal_progress]
            + subset["goal_progress_pct"].tolist()
        )

        worth_values = (
            [initial_net_worth]
            + subset["net_worth"].tolist()
        )

        color = config["color"]
        label = config["label"]

        # Cash timeline
        fig.add_trace(
            go.Scatter(
                x=x,
                y=cash_values,
                name=label,
                legendgroup=scenario,
                mode="lines+markers",
                line=dict(
                    color=color,
                    width=3
                ),
                marker=dict(size=5)
            ),
            row=1,
            col=1
        )

        # Goal progress timeline
        fig.add_trace(
            go.Scatter(
                x=x,
                y=goal_values,
                name=label,
                legendgroup=scenario,
                showlegend=False,
                mode="lines",
                line=dict(
                    color=color,
                    width=3
                )
            ),
            row=1,
            col=2
        )

        # Net worth timeline
        fig.add_trace(
            go.Scatter(
                x=x,
                y=worth_values,
                name=label,
                legendgroup=scenario,
                showlegend=False,
                mode="lines",
                line=dict(
                    color=color,
                    width=3
                )
            ),
            row=2,
            col=2
        )

        # Summary report
        final = subset.iloc[-1]

        summary_rows.append({
            "user_id": user_id,
            "scenario": scenario,
            "horizon_months": months,
            "currency": currency,
            "initial_cash": initial_cash,
            "final_cash": final[
                "projected_cash_position"
            ],
            "cash_change": (
                final["projected_cash_position"]
                - initial_cash
            ),
            "final_loan_balance": final[
                "loan_balance"
            ],
            "goal_progress_pct": final[
                "goal_progress_pct"
            ],
            "final_net_worth": final[
                "net_worth"
            ],
            "final_risk_level": final[
                "risk_level"
            ]
        })

    # ======================================
    # 4. LOAN REPAYMENT TIMELINE
    # ======================================

    # Same debt schedule in all three scenarios
    baseline = (
        df[df["scenario"] == "baseline"]
        .sort_values("month")
    )

    fig.add_trace(
        go.Scatter(
            x=[0] + baseline["month"].tolist(),
            y=[initial_debt]
              + baseline["loan_balance"].tolist(),
            name="Outstanding Debt",
            showlegend=False,
            mode="lines+markers",
            line=dict(
                color="#FBBF24",
                width=3
            ),
            marker=dict(size=5),
            fill="tozeroy",
            fillcolor="rgba(251,191,36,0.08)"
        ),
        row=2,
        col=1
    )

    # ======================================
    # 5. FINOVA DARK THEME
    # ======================================

    fig.update_layout(
        title=dict(
            text=(
                f"FINOVA AI | Financial Digital Twin"
                f"<br><sup>User {user_id} | "
                f"{months}-Month Financial Simulation"
                f" | {currency}</sup>"
            ),
            x=0.5,
            xanchor="center",
            font=dict(size=22)
        ),
        template="plotly_dark",
        paper_bgcolor="#0B1020",
        plot_bgcolor="#141B30",
        font=dict(
            family="Arial",
            color="#E5E7EB"
        ),
        height=850,
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.13,
            xanchor="center",
            x=0.5
        ),
        margin=dict(
            l=65,
            r=40,
            t=115,
            b=95
        )
    )

    fig.update_xaxes(
        title_text="Month",
        gridcolor="#283149",
        zeroline=False,
        dtick=max(1, months // 12)
    )

    fig.update_yaxes(
        gridcolor="#283149",
        zeroline=False
    )

    for row, col in [(1, 1), (2, 1), (2, 2)]:
        fig.update_yaxes(
            tickprefix=f"{currency} ",
            tickformat=",.0f",
            row=row,
            col=col
        )

    fig.update_yaxes(
        ticksuffix="%",
        row=1,
        col=2
    )

    # Goal target reference
    fig.add_hline(
        y=100,
        line_dash="dot",
        line_color="#94A3B8",
        row=1,
        col=2
    )

    # ======================================
    # 6. EXPORT INTERACTIVE HTML
    # ======================================

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    html_path = (
        OUTPUT_DIR
        / f"twin_{user_id}_{months}m.html"
    )

    summary_path = (
        OUTPUT_DIR
        / f"twin_{user_id}_{months}m_summary.csv"
    )

    fig.write_html(
        str(html_path),
        include_plotlyjs=True,
        full_html=True
    )

    summary = pd.DataFrame(summary_rows)

    summary.to_csv(
        summary_path,
        index=False
    )

    print("\n===== FINOVA AI VISUALIZATION =====")
    print("User:", user_id)
    print("Simulation Horizon:", months)
    print("\nScenario Summary:")

    print(
        summary[
            [
                "scenario",
                "final_cash",
                "goal_progress_pct",
                "final_risk_level"
            ]
        ].to_string(index=False)
    )

    print("\nInteractive HTML:")
    print(html_path)

    print("\nSummary CSV:")
    print(summary_path)

    print("\nVisualization completed successfully!")


# ==========================================
# 7. EXECUTION
# ==========================================

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

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
            "Months must be between 1 and 120"
        )

    create_visualization(
        args.user_id,
        args.months
    )
