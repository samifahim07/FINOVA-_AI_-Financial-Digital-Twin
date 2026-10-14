# FINOVA AI — Financial Digital Twin

### Intelligent Financial Modeling, Dynamic Simulation, and Future Scenario Analysis

FINOVA AI Financial Digital Twin is a financial intelligence module designed to create a virtual representation of an individual's financial condition, evaluate financial behavior, simulate future outcomes, and support informed financial decision-making.

The system combines structured financial profiles, deterministic financial simulations, debt amortization, goal tracking, and rule-based risk assessment to explore how different spending behaviors may affect an individual's financial future.

This module was developed as part of **FINOVA AI — Personal Financial Intelligence**, an AI-powered personal finance management project.

---

## 1. Project Overview

Traditional financial dashboards primarily display historical transactions, income, expenses, and account balances.

The Financial Digital Twin extends these capabilities through scenario-based financial modeling.

It represents an individual's financial condition using financial state variables, including income, expenses, savings, assets, liabilities, emergency reserves, and financial goals.

The system then simulates how these variables may evolve over time under different financial assumptions.

### Core Objectives

- Construct individual financial profiles from structured financial data.
- Analyze financial behavior and financial health.
- Simulate changes in cash flow, outstanding debt, and net worth.
- Compare alternative financial scenarios.
- Evaluate financial goal progress and affordability.
- Detect potential financial risks using transparent rules.
- Visualize projected financial conditions through interactive timelines.
- Provide REST API endpoints for integration with larger financial applications.

## 2. Key Features

### 2.1 Financial Digital Twin Generation

Creates an individual financial snapshot containing:

- Monthly income and expenses
- Monthly net cash flow
- Current cash balance
- Total assets and liabilities
- Net worth
- Emergency fund
- Outstanding loan balance
- Financial goals and target periods

Each profile is identified by a unique user ID.

### 2.2 Financial Health Assessment

Calculates several financial indicators, including:

| Financial Indicator | Calculation |
|---|---|
| Savings Rate | Monthly Cash Flow / Monthly Income |
| Expense Ratio | Monthly Expenses / Monthly Income |
| Debt Service Ratio | Monthly Loan Payments / Monthly Income |
| Emergency Fund Coverage | Emergency Fund / Monthly Expenses |
| Debt-to-Asset Ratio | Total Debt / Total Assets |
| Net Worth | Total Assets − Total Debt |

These indicators provide a structured view of the user's current financial condition.

### 2.3 Dynamic Financial Simulation

The simulation engine models financial changes across multiple future months.

Supported simulation horizons range from 1 to 120 months.

Each simulated month updates:

- Projected cash position
- Monthly income and living expenses
- Monthly cash flow
- Loan interest and repayments
- Remaining outstanding debt
- Emergency reserves
- Financial goal contributions
- Projected net worth
- Financial risk indicators

The simulation uses deterministic financial calculations based on defined assumptions rather than claiming to predict future market or individual behavior with certainty.

### 2.4 Financial Scenario Intelligence

Three alternative scenarios are supported.

| Scenario | Assumption |
|---|---|
| Baseline | Existing income and spending behavior remain unchanged |
| Save More | Living expenses decrease by 10% |
| Spend More | Living expenses increase by 15% |

The scenarios are independently simulated and compared against the baseline.

**Example — User U0001, 12-Month Simulation**

| Scenario | Projected Cash Balance | Goal Progress |
|---|---:|---:|
| Baseline | BDT 690,986.00 | 2.96% |
| Save More | BDT 834,075.20 | 11.18% |
| Spend More | BDT 476,352.20 | 0.00% |

Under the simulated assumptions, reducing living expenses by 10% produces an additional BDT 143,089.20 compared with the baseline.

These values are illustrative outputs generated from a synthetic financial profile.

### 2.5 Financial Risk Assessment

The Digital Twin evaluates five financial risk conditions:

1. Negative monthly cash flow
2. Insufficient emergency fund coverage
3. High debt service burden
4. Negative net worth
5. Financial goal funding gap

A rule-based assessment classifies the financial condition into three categories:

- **LOW:** No active risk flags
- **MODERATE:** One or two active risk flags
- **HIGH:** Three or more active risk flags

The risk categories are heuristic indicators and should not be interpreted as validated credit ratings or financial risk probabilities.

### 2.6 Financial Goal Intelligence

The system tracks financial targets such as:

- Emergency fund accumulation
- Education savings
- Vehicle purchase
- Home purchase
- Business establishment
- Travel savings

The engine calculates current progress, remaining target amount, required monthly contributions, and feasibility based on the available financial surplus.

### 2.7 Interactive Financial Timeline

The visualization module presents financial scenarios through interactive charts.

Supported visualizations include:

- Cash Position Timeline
- Projected Net Worth
- Outstanding Loan Balance
- Financial Goal Progress

Users can compare scenarios, change projection periods, and inspect individual months.

The integrated FINOVA AI interface supports animated backgrounds, responsive layouts, and two visual themes:

**Minimal Finance:** A clean, light financial dashboard.

**Liquid Intelligence:** A dark interface featuring animated gradients, subtle visual effects, and financial intelligence components.

Reduced-motion preferences are supported.

---

## 3. Dataset

### Synthetic Financial Profiles V2

The Financial Digital Twin uses a custom-generated dataset designed for simulation development, validation, and demonstration.

| Attribute | Value |
|---|---|
| Dataset | Financial Profiles V2 |
| Total Profiles | 500 |
| Total Columns | 21 |
| Format | CSV |
| Currency | BDT |
| Data Type | Synthetic |
| Missing Values | 0 |
| Duplicate User IDs | 0 |

### Financial Personas

The dataset contains four synthetic financial personas.

| Persona | Number of Profiles |
|---|---:|
| Working Professional | 177 |
| Family Household | 142 |
| Early Career | 125 |
| High Income | 56 |
| **Total** | **500** |

### Financial Profile Attributes

The dataset contains the following columns:

- `user_id`
- `persona`
- `currency`
- `monthly_income`
- `living_expense`
- `monthly_loan_payment`
- `monthly_expense`
- `monthly_cash_flow`
- `monthly_savings`
- `current_balance`
- `emergency_fund`
- `total_debt`
- `loan_apr_pct`
- `loan_remaining_months`
- `total_assets`
- `net_worth`
- `financial_goal`
- `target_amount`
- `goal_saved_so_far`
- `target_months`
- `data_source`

### Synthetic Financial Risk Distribution

The generated dataset contains:

| Indicator | Profiles |
|---|---:|
| High Debt Burden | 151 |
| Negative Monthly Cash Flow | 99 |
| Negative Net Worth | 73 |

These distributions result from the synthetic data generation rules. They are not population-level financial statistics.

---

## 4. System Architecture

The Financial Digital Twin follows a modular architecture.

**Layer 1 — Financial Data Layer**

Stores individual synthetic financial profiles and their initial financial conditions.

**Layer 2 — Financial State Engine**

Calculates current financial indicators, financial goals, net worth, and risk conditions.

**Layer 3 — Dynamic Simulation Engine**

Models future monthly financial conditions, including cash flow evolution, debt amortization, reserve allocation, and alternative spending scenarios.

**Layer 4 — Financial Intelligence Layer**

Evaluates projected financial risk and financial goal progress.

**Layer 5 — API Layer**

Exposes financial profiles, digital twin snapshots, and simulation results through FastAPI endpoints.

**Layer 6 — Visualization Layer**

Presents financial intelligence through interactive charts, financial KPI cards, scenario comparisons, and animated interfaces.

### Technology Stack

| Layer | Technologies |
|---|---|
| Programming Language | Python |
| Data Processing | Pandas, NumPy |
| Exploratory Analysis | Matplotlib |
| Standalone Visualization | Plotly |
| Financial Simulation | Rule-based deterministic modeling |
| Backend API | FastAPI |
| ASGI Server | Uvicorn |
| Integrated Frontend | React, TypeScript, Vite |
| UI Styling | Tailwind CSS, Custom CSS |
| Data Format | CSV, JSON |
| Automated Verification | Python assertions and accounting checks |

---

## 5. Project Structure

```text
FINOVA-AI-Financial-Digital-Twin/
|
|-- data/
|   |-- raw/
|   |   |-- financial_profiles.csv
|   |   |-- financial_profiles_v2.csv
|   |
|   |-- processed/
|       |-- financial_profiles_enriched.csv
|
|-- notebooks/
|
|-- reports/
|   |-- figures/
|   |-- simulations/
|   |-- visualizations/
|
|-- src/
|   |-- __init__.py
|   |-- api.py
|   |-- data_generator.py
|   |-- data_generator_v2.py
|   |-- data_validation.py
|   |-- financial_eda.py
|   |-- twin_engine.py
|   |-- simulator.py
|   |-- visualize_twin.py
|
|-- tests/
|   |-- test_full_engine.py
|   |-- test_final_verification.py
|
|-- requirements.txt
|-- README.md
```

---

## 6. Installation and Setup

### Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/FINOVA-AI-Financial-Digital-Twin.git
cd FINOVA-AI-Financial-Digital-Twin
```

Replace `YOUR_USERNAME` with your GitHub username.

### Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.\.venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

For API execution, ensure that FastAPI and Uvicorn are installed:

```bash
pip install fastapi uvicorn
```

---

## 7. Running the Financial Digital Twin

### Generate Financial Profiles

```bash
python src/data_generator_v2.py
```

This generates 500 synthetic financial profiles.

### Run Financial State Analysis

```bash
python src/twin_engine.py U0001
```

The engine calculates the selected user's financial condition and exports a financial twin snapshot.

### Run a 12-Month Simulation

```bash
python src/simulator.py U0001 --months 12
```

### Run a 36-Month Simulation

```bash
python src/simulator.py U0047 --months 36
```

### Generate Interactive Financial Visualizations

```bash
python src/visualize_twin.py U0001 --months 12
```

The visualization script exports interactive HTML charts and summary reports.

---

## 8. REST API

The standalone module provides REST API endpoints implemented using FastAPI.

### Start the Standalone API

```bash
python -m uvicorn src.api:app --reload --port 8001
```

API documentation is available at:

`http://127.0.0.1:8001/docs`

### Main Application Integration

The Financial Digital Twin has also been integrated into the FINOVA AI main FastAPI backend using an independent API router.

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/v1/twin/users` | Retrieve available financial profiles |
| GET | `/api/v1/twin/{user_id}` | Generate an individual financial twin |
| GET | `/api/v1/twin/{user_id}/simulate` | Simulate future financial scenarios |

Example:

```text
GET /api/v1/twin/U0001/simulate?months=12
```

### Simulation API Response

The integrated API returns:

- User identifier and currency
- Simulation horizon
- Financial model metadata
- Baseline scenario summary
- Save More scenario summary
- Spend More scenario summary
- Monthly financial state timelines
- Financial risk indicators

The main FINOVA AI backend serves these endpoints through port `8000` in the local development environment.

---

## 9. Financial Modeling Methodology

### Monthly Cash Flow

**Monthly Cash Flow = Monthly Income − Total Monthly Expenses**

### Net Worth

**Net Worth = Total Assets − Total Liabilities**

### Emergency Fund Coverage

**Emergency Coverage = Emergency Fund / Monthly Expenses**

### Loan Amortization

Monthly loan interest is calculated using the outstanding principal and annual interest rate.

**Monthly Interest = Outstanding Loan Balance × (Annual Interest Rate / 12)**

The outstanding loan balance is updated after accounting for monthly interest and the actual payment.

### Goal Progress

**Goal Progress (%) = Amount Saved / Target Amount × 100**

### Financial Scenario Modeling

Financial conditions evolve independently for each scenario.

The engine calculates monthly cash flow, updates loan balances, allocates available funds, evaluates financial goals, and produces a financial state for each simulated month.

Emergency fund accounting is handled separately to avoid double counting when the financial goal itself is an emergency fund.

---

## 10. Automated Testing and Verification

The Financial Digital Twin was evaluated using automated simulation and financial consistency checks.

### Basic Engine Audit

| Metric | Result |
|---|---:|
| Financial Profiles Tested | 500 |
| Profiles Passed | 500 |
| Profiles Failed | 0 |

### Final Financial Verification

The final audit evaluated three scenarios across three simulation horizons.

| Test Configuration | Value |
|---|---|
| Users | 500 |
| Scenarios per User | 3 |
| Simulation Horizons | 12, 36, 120 Months |
| Total Scenario Executions | 4,500 |
| Passed Executions | 4,500 |
| Failed Checks | 0 |

### Verified Conditions

The verification process checks:

- Monthly cash-flow consistency
- Loan repayment calculations
- Non-negative outstanding loan balances
- Emergency fund accounting
- Financial goal balance constraints
- Projected net-worth consistency
- Unfunded cash gap calculations
- Goal progress calculations
- Scenario comparison consistency
- Finite financial values over simulation horizons

These tests verify important calculation and accounting properties of the synthetic simulation engine.

They do not establish real-world financial forecasting accuracy or guarantee that every possible financial condition has been modeled.

### Run Automated Tests

```bash
python tests/test_full_engine.py
python tests/test_final_verification.py
```

---

## 11. Integration with FINOVA AI

The Financial Digital Twin operates as the fourth major financial intelligence module within the FINOVA AI application.

The integrated application includes:

1. Financial Dashboard and Transaction Analytics
2. Subscription Detection and Intelligence
3. Predictive Financial Forecasting
4. Financial Digital Twin

The Financial Digital Twin module is connected to the existing FastAPI backend through a dedicated router.

The React frontend provides access to financial profiles, financial indicators, risk assessments, scenario comparisons, and interactive future timelines.

The original Financial Dashboard and the Digital Twin currently use separate demonstration datasets.

The Dashboard uses historical household transaction data, while the Financial Digital Twin uses synthetic financial profiles.

The modules are not presented as financial records belonging to the same real individual.

---

## 12. Current Limitations

The current implementation is designed for financial simulation, prototyping, and demonstration.

Important limitations include:

- Financial profiles are synthetically generated.
- Financial risk classification uses configurable rules, not a validated risk prediction model.
- Future outcomes are determined by predefined simulation assumptions.
- Income growth, inflation, and investment returns are not dynamically modeled in the current simulator.
- Independent financial datasets are not merged into a verified individual financial history.
- Real-time bank synchronization is not implemented.
- The Financial Digital Twin is not yet connected to the project's trained forecasting models.
- Real-user authentication and production authorization are outside the current standalone prototype.

Financial projections are illustrative and should not be treated as guaranteed future outcomes or personalized financial advice.

---

## 13. Future Development

Planned areas for further development include:

- Integration with machine-learning financial forecasting models
- Personalized financial profile creation
- User-controlled income and expense assumptions
- Inflation-aware financial simulation
- Investment growth and asset-value modeling
- Advanced goal optimization
- Financial stress testing
- Personalized financial recommendations
- Secure user authentication and authorization
- Real financial transaction integration
- Continuous financial twin state updates

These improvements aim to extend the deterministic prototype toward a more adaptive, data-driven financial intelligence system.

---

## 14. Project Status

**Current Status: Functional Prototype — Backend Integrated**

The following components have been implemented and tested:

- Financial profile generation
- Financial state calculation
- Financial risk assessment
- Dynamic financial simulation
- Scenario comparison
- Financial goal tracking
- Interactive financial visualization
- REST API integration
- Automated financial verification
- Integration with the FINOVA AI React frontend

The module is suitable for demonstrating rule-based financial simulations and financial scenario analysis.

Production financial data integration and real-world predictive validation remain future development objectives.

---

## 15. Disclaimer

This project is intended for educational, research, software development, and financial technology demonstration purposes.

All financial profiles used in the current prototype are synthetic.

Financial risk assessments and future projections are generated from assumptions and simplified financial models.

The project does not provide regulated financial advice, guaranteed investment outcomes, or verified creditworthiness assessments.

---

## 16. Project

**Project:** FINOVA AI — Personal Financial Intelligence

**Module:** Financial Digital Twin

**Category:** Financial Technology, Financial Simulation, Personal Finance Intelligence

**Development:** Python, FastAPI, React, TypeScript

**Dataset:** Synthetic Financial Profiles V2

**Status:** Functional Prototype

---

FINOVA AI Financial Digital Twin demonstrates how financial state modeling, dynamic simulation, scenario analysis, and interactive visualization can help users better understand the potential consequences of their financial decisions.

The objective is not only to describe an individual's current financial position, but also to make possible future financial outcomes more understandable, transparent, and actionable.
