import random

def run_simulation(
    income,
    expenses,
    months,
    initial_savings,
    inflation_rate,
    investment_return,
    salary_growth
):

    balance = initial_savings

    history = []

    emergencies = []

    bankrupt = False

    for month in range(months):

        # Monthly inflation
        monthly_inflation = inflation_rate / 100 / 12
        expenses *= (1 + monthly_inflation)
        monthly_salary_growth = salary_growth / 100 / 12
        income *= (1 + monthly_salary_growth)

        # Monthly income/expense update
        balance += income - expenses
        monthly_return = investment_return / 100 / 12
        monthly_salary_growth = salary_growth / 100 / 12
        income *= (1 + monthly_salary_growth)
        balance *= (1 + monthly_return)

        # Random emergency event
        if random.random() < 0.2:

            emergency_cost = random.randint(100, 1000)

            balance -= emergency_cost

            emergencies.append(
                f"Emergency in month {month + 1}: -${emergency_cost}"
            )

        # Bankruptcy detection
        if balance < 0:
            bankrupt = True

        history.append(balance)

    return history, balance, emergencies, bankrupt