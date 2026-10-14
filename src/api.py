
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from .twin_engine import load_profiles, build_financial_twin
from .simulator import SCENARIOS, simulate_profile

app = FastAPI(
    title="FINOVA AI - Financial Digital Twin",
    version="1.0.0",
    description="Financial profile and simulation API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_methods=["GET"],
    allow_headers=["*"]
)


def get_profile(user_id):
    df = load_profiles()
    selected = df[df["user_id"] == user_id]

    if selected.empty:
        raise HTTPException(
            status_code=404,
            detail=f"User {user_id} not found"
        )

    return selected.iloc[0]


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "FINOVA Financial Digital Twin",
        "version": "1.0.0"
    }


@app.get("/api/v1/twin/users")
def get_users(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    df = load_profiles()

    users = df[
        ["user_id", "persona", "financial_goal", "currency"]
    ].iloc[offset:offset + limit]

    return {
        "total_users": len(df),
        "users": users.to_dict(orient="records")
    }


@app.get("/api/v1/twin/{user_id}")
def get_twin(user_id: str):
    profile = get_profile(user_id)
    return build_financial_twin(profile)


@app.get("/api/v1/twin/{user_id}/simulate")
def simulate_twin(
    user_id: str,
    months: int = Query(12, ge=1, le=120)
):
    profile = get_profile(user_id)

    scenarios = {}

    for name, multiplier in SCENARIOS.items():
        scenarios[name] = simulate_profile(
            profile,
            months,
            multiplier
        )

    return {
        "user_id": user_id,
        "currency": str(profile["currency"]),
        "months": months,
        "model_type": "deterministic_simulation",
        "scenarios": scenarios
    }
