from simulator import run_simulation


def run_monte_carlo(
    simulations,
    income,
    expenses,
    months,
    initial_savings,
    inflation_rate,
    investment_return,
    salary_growth,
    savings_goal
):

    final_balances = []

    bankruptcies = 0

    goals_reached = 0

    for _ in range(simulations):

        history, final_balance, emergencies, bankrupt = run_simulation(
            income,
            expenses,
            months,
            initial_savings,
            inflation_rate,
            investment_return,
            salary_growth
        )

        final_balances.append(final_balance)

        if bankrupt:
            bankruptcies += 1

        if final_balance >= savings_goal:
            goals_reached += 1

    average_balance = sum(final_balances) / simulations

    bankruptcy_probability = (
        bankruptcies / simulations
    ) * 100

    goal_probability = (
        goals_reached / simulations
    ) * 100

    return (
        average_balance,
        bankruptcy_probability,
        goal_probability,
        final_balances
    )