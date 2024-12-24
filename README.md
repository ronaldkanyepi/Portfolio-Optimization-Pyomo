# Portfolio Optimization with Streamlit and Pyomo

This project optimizes stock portfolios by selecting up to 10 tickers and a custom date range. Using **Pyomo** for optimization, it minimizes risk while targeting a desired return. The app displays portfolio allocations, expected returns, risk ceilings, and stock correlation heatmaps, with data sourced from **yfinance**.

## Features

- **Stock Ticker Selection**: Select up to 10 stock tickers.
- **Date Range**: Choose a custom start and end date.
- **Optimization**: Minimize portfolio risk while maintaining a desired return.
- **Display**: View portfolio allocation, max return, risk ceiling, and a heatmap of stock correlations.

## Why Start and End Dates are Required
- The start and end dates define the period for which stock data is fetched and analyzed. These dates allow the app to calculate historical returns and perform portfolio optimization based on the chosen timeframe. By selecting specific dates, users can analyze stocks under different market conditions and tailor the optimization to their desired time horizon.

## Setup Instructions

### 1. Create a Virtual Environment

```bash
python -m venv venv
```
Activate the virtual environment:
- **Windows**: `venv\Scripts\activate`
- **MacOS/Linux**: `source venv/bin/activate`

### 2. Install Dependencies
`pip install -r requirements.txt`

- Or manually install:
`pip install streamlit pyomo yfinance seaborn matplotlib numpy pandas`

### 3. Install IPOPT Solver
**Windows**: Download IPOPT from COIN-OR IPOPT and add ipopt.exe to your PATH.

### 3. Install IPOPT Solver
**Windows**: Download IPOPT from COIN-OR IPOPT https://github.com/coin-or/Ipopt/releases and add ipopt.exe to your PATH.

**MacOS/Linux**: Install using brew (MacOS) or apt-get (Ubuntu).: Install using brew (MacOS) or apt-get (Ubuntu).

### 4. Run the App
streamlit run main.py
