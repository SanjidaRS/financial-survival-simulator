import pandas as pd
import plotly.express as px


def create_balance_chart(history):

    df = pd.DataFrame({
        "Month": list(range(1, len(history) + 1)),
        "Balance": history
    })

    fig = px.line(
        df,
        x="Month",
        y="Balance",
        title="Savings Growth Over Time"
    )

    return fig