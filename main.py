import yfinance as yf
import pandas as pd
import pyomo.environ as pyo
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

# Streamlit app interface
st.title("Portfolio Optimization")

# Allow the user to select tickers
# Predefined list of tickers
tickers_list = [
    'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA',  # Technology
    'MRK', 'PFE', 'JNJ', 'ABBV', 'AMGN',  # Healthcare
    'PG', 'KO', 'PEP', 'CL', 'MCD',  # Consumer Goods
    'XOM', 'CVX', 'SLB', 'COP',  # Energy
    'JPM', 'GS', 'C', 'BAC',  # Finance
    'BA', 'GE', 'CAT', 'LMT',  # Industrials
    'DIS', 'NFLX', 'AMT', 'VZ',  # Consumer Services
    'DUK', 'AEE', 'SO', 'XEL'  # Utilities
]

# Allow the user to select up to 10 tickers using multiselect
selected_tickers = st.multiselect(
    "Select Stock Tickers (up to 10)",
    tickers_list,
    default=['AAPL', 'MSFT', 'GOOGL'],
    max_selections=10
)

# Check if the user selected more than 10 tickers
if len(selected_tickers) > 10:
    st.warning("You can select up to a maximum of 10 tickers.")

# Allow the user to select the start and end dates
start_date = st.date_input("Start Date", pd.to_datetime('2019-10-01'))
end_date = st.date_input("End Date", pd.to_datetime('2024-10-31'))

submit = st.button('Submit')

if submit:
    data = yf.download(selected_tickers, start=start_date, end=end_date, interval="1mo")

    # Extract the 'Adj Close' prices for all tickers
    df = data.xs('Adj Close', level='Price', axis=1)

    # Format the index
    df.index = df.index.strftime('%b-%Y')

    # Calculate the month-to-month percentage change of the adjusted closing prices
    df = df.pct_change()

    # Drop the NaN values caused by pct_change
    df = df.dropna()

    # Portfolio optimization model using Pyomo
    model = pyo.ConcreteModel('Portfolio Management')

    model.stocks = pyo.Set(initialize=df.columns)

    model.p = pyo.Var(model.stocks, domain=pyo.NonNegativeReals)


    # Constraints and objective
    def mean_return(model, reward_floor):
        return sum(model.p[i] * df.loc[:, i].mean() for i in model.stocks) >= reward_floor


    def portfolio_variance(model):
        return sum(np.cov(df.loc[:, i], df.loc[:, j])[0, 1] * model.p[i] * model.p[j] for i in model.stocks for j in
                   model.stocks)


    def sum_allocation(model):
        return sum(model.p[i] for i in model.stocks) == 1


    model.min_risk = pyo.Objective(rule=portfolio_variance, sense=pyo.minimize)
    model.min_reward = pyo.Constraint(rule=mean_return(model, reward_floor=0.01))
    model.sum_allocs = pyo.Constraint(rule=sum_allocation)

    # Solve the model
    solver = pyo.SolverFactory('ipopt', executable='C:/ProgramData/anaconda3/envs/PS3/Library/bin/ipopt.exe')
    solver.solve(model)

    # Extract the optimized weights for the portfolio
    optimized_weights = {i: model.p[i].value for i in model.stocks}

    st.write("### Optimized Portfolio Weights (Allocation):")
    weights_df = pd.DataFrame(list(optimized_weights.items()), columns=["Stock", "Weight"])
    weights_df["Weight"] = weights_df["Weight"] * 100
    weights_df["Weight"] = weights_df["Weight"].round(2)

    # Add a total row to the DataFrame
    total_weight = weights_df["Weight"].sum().round(1)
    weights_df["Weight"] = weights_df["Weight"].astype(str) + ' %'
    total_weight = str(total_weight) + ' %'
    total_row = pd.DataFrame([["Total", total_weight]], columns=["Stock", "Weight"])
    weights_df = pd.concat([weights_df, total_row], ignore_index=True)


    st.dataframe(weights_df, width=600)


    col1, col2 = st.columns(2)

    with col1:
        st.write("### Max Return Expected:")
        st.write(f"{model.min_reward():.4f}")

    with col2:
        st.write("### Risk Ceiling:")
        st.write(f"{model.min_risk():.6f}")

    st.subheader("Portfolio Return vs Risk")
    fig = plt.figure(figsize=(10, 6))
    sns.heatmap(df.corr(), annot=True, cmap="coolwarm")
    st.pyplot(fig)


