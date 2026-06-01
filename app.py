import streamlit as st
import plotly.express as px
import pandas as pd

from monte_carlo import run_monte_carlo
from simulator import run_simulation
from charts import create_balance_chart


# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(
    page_title="Financial Survival Simulator",
    page_icon="",
    layout="wide"
)

st.title(" Financial Survival Simulator")

st.caption(
    "Predict possible financial futures using simulation and probabilistic modeling."
)


# =========================================
# SIDEBAR
# =========================================

st.sidebar.header("Simulation Settings")

# Scenario Selection
scenario = st.sidebar.selectbox(
    "Choose Scenario",
    [
        "Custom",
        "Student Life",
        "High Income Professional",
        "Financially Struggling",
        "Aggressive Investor"
    ]
)

# Default Values
income_default = 3500
expenses_default = 2000
savings_default = 1000
goal_default = 10000
investment_default = 5

# Scenario Presets
if scenario == "Student Life":
    income_default = 1800
    expenses_default = 1600
    savings_default = 500

elif scenario == "High Income Professional":
    income_default = 8000
    expenses_default = 3500
    savings_default = 15000

elif scenario == "Financially Struggling":
    income_default = 1800
    expenses_default = 2200
    savings_default = 200

elif scenario == "Aggressive Investor":
    income_default = 5000
    expenses_default = 2500
    savings_default = 10000
    investment_default = 12

# Inputs
income = st.sidebar.number_input(
    "Monthly Income",
    min_value=0,
    value=income_default,
    help="Your average monthly earnings."
)

expenses = st.sidebar.number_input(
    "Monthly Expenses",
    min_value=0,
    value=expenses_default,
    help="Your average monthly spending."
)

initial_savings = st.sidebar.number_input(
    "Initial Savings",
    min_value=0,
    value=savings_default,
    help="Money already saved before simulation starts."
)

savings_goal = st.sidebar.number_input(
    "Savings Goal",
    min_value=0,
    value=goal_default,
    help="Your target future savings amount."
)

inflation_rate = st.sidebar.slider(
    "Yearly Inflation Rate (%)",
    0,
    20,
    3,
    help="Inflation slowly increases expenses over time."
)

investment_return = st.sidebar.slider(
    "Yearly Investment Return (%)",
    0,
    20,
    investment_default,
    help="Expected yearly investment growth."
)

salary_growth = st.sidebar.slider(
    "Yearly Salary Growth (%)",
    0,
    15,
    2,
    help="Expected yearly salary increase."
)

months = st.sidebar.slider(
    "Number of Months",
    1,
    60,
    12
)

simulations = st.sidebar.slider(
    "Monte Carlo Simulations",
    100,
    5000,
    1000,
    step=100,
    help="Higher simulations improve prediction accuracy."
)

st.sidebar.markdown("---")

st.sidebar.info(
    """
    This simulator predicts possible financial futures
    using probabilistic Monte Carlo analysis.
    """
)

# =========================================
# SIDEBAR HELP SECTIONS
# =========================================

with st.sidebar.expander(" How It Works"):

    st.write("""
    • Enter your financial details.

    • The simulator predicts your financial future month-by-month.

    • Random emergencies may occur.

    • Inflation increases expenses over time.

    • Investments and salary growth may improve savings.

    • Monte Carlo analysis runs many possible futures
      to estimate financial risk.
    """)

with st.sidebar.expander(" FAQ"):

    st.write("""
    Q: What is Monte Carlo simulation?

    A: It runs hundreds of randomized financial futures
    to estimate probabilities and risks.

    Q: What does bankruptcy risk mean?

    A: The percentage chance your balance goes below zero.

    Q: Why are results different every run?

    A: Random emergency events create uncertainty,
    similar to real life.

    Q: What affects financial health most?

    A: High expenses relative to income.
    """)

with st.sidebar.expander(" Financial Terms"):

    st.write("""
    • Inflation:
      Rising costs over time.

    • Investment Return:
      Growth earned from investments.

    • Salary Growth:
      Expected yearly increase in income.

    • Savings Goal:
      Desired future balance.

    • Bankruptcy:
      Balance dropping below zero.
    """)


# =========================================
# RUN SIMULATION
# =========================================

history, final_balance, emergencies, bankrupt = run_simulation(
    income,
    expenses,
    months,
    initial_savings,
    inflation_rate,
    investment_return,
    salary_growth
)

(
    average_balance,
    bankruptcy_probability,
    goal_probability,
    final_balances
) = run_monte_carlo(
    simulations,
    income,
    expenses,
    months,
    initial_savings,
    inflation_rate,
    investment_return,
    salary_growth,
    savings_goal
)


# =========================================
# CREATE CHARTS
# =========================================

line_chart = create_balance_chart(history)

histogram_fig = px.histogram(
    x=final_balances,
    nbins=30,
    title="Distribution of Final Balances"
)

expense_data = pd.DataFrame({
    "Category": ["Expenses", "Savings"],
    "Amount": [expenses, income - expenses]
})

pie_chart = px.pie(
    expense_data,
    names="Category",
    values="Amount",
    title="Income Breakdown"
)


# =========================================
# FINANCIAL HEALTH SCORE
# =========================================

if income > 0:
    stress_score = expenses / income
else:
    stress_score = 0


# =========================================
# TABS
# =========================================

tab1, tab2, tab3 = st.tabs([
    " Dashboard",
    " Analytics",
    " Simulation Details"
])


# =========================================
# DASHBOARD TAB
# =========================================

with tab1:

    st.header("Financial Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Final Balance",
        f"${final_balance:.2f}"
    )

    col2.metric(
        "Goal Success Rate",
        f"{goal_probability:.1f}%"
    )

    col3.metric(
        "Bankruptcy Risk",
        f"{bankruptcy_probability:.1f}%"
    )

    st.info(f"""
    Scenario Summary:

    • Monthly Income: ${income}
    • Monthly Expenses: ${expenses}
    • Inflation Rate: {inflation_rate}%
    • Investment Return: {investment_return}%
    • Salary Growth: {salary_growth}%
    """)

    st.success(
        f"Final Balance After {months} Months: ${final_balance:.2f}"
    )

    # Savings Goal
    if final_balance >= savings_goal:

        st.success(
            f"You reached your savings goal of ${savings_goal}!"
        )

    else:

        remaining = savings_goal - final_balance

        st.error(
            f"You are ${remaining:.2f} away from your goal."
        )

    # Bankruptcy
    if bankrupt:
        st.error("You went bankrupt during the simulation.")

    # Financial Health
    st.subheader("Financial Health")

    st.caption("""
    Financial health is based on the ratio between
    monthly expenses and income.
    """)

    if stress_score < 0.5:

        st.success("🟢 Financially Healthy")

    elif stress_score < 0.8:

        st.warning("🟡 Moderate Financial Stress")

    else:

        st.error("🔴 High Financial Stress")

    # Risk Interpretation
    st.subheader("Risk Interpretation")

    if bankruptcy_probability < 20:

        st.success("Low financial risk.")

    elif bankruptcy_probability < 50:

        st.warning("Moderate financial risk.")

    else:

        st.error("High probability of financial instability.")


# =========================================
# ANALYTICS TAB
# =========================================

with tab2:

    st.header("Analytics")

    st.plotly_chart(line_chart)

    st.plotly_chart(histogram_fig)

    st.plotly_chart(pie_chart)

    st.subheader("Monte Carlo Analysis")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Average Final Balance",
        f"${average_balance:.2f}"
    )

    col2.metric(
        "Bankruptcy Probability",
        f"{bankruptcy_probability:.1f}%"
    )

    col3.metric(
        "Goal Achievement Rate",
        f"{goal_probability:.1f}%"
    )


# =========================================
# DETAILS TAB
# =========================================

with tab3:

    st.header("Simulation Events")

    if emergencies:

        for event in emergencies:
            st.warning(event)

    else:

        st.success("No emergencies occurred.")

    st.subheader("Download Results")

    results_df = pd.DataFrame({
        "Month": list(range(1, len(history) + 1)),
        "Balance": history
    })

    st.download_button(
        label="Download Simulation Results",
        data=results_df.to_csv(index=False),
        file_name="simulation_results.csv",
        mime="text/csv"
    )