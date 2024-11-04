# -*- coding: utf-8 -*-
"""Trend_analyser.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/16Ct6w8V2LwZ0SuTlEuYP3t1RfYDKCQep
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import math
from scipy.stats import norm  # Importing the norm function from scipy.stats

# Define the ticker symbol for Nifty 50
ticker_symbol = "^NSEI"  # Yahoo Finance symbol for Nifty 50

# Define the date range for the last 30 days
end_date = datetime.today()
start_date = end_date - timedelta(days=30)

# Fetch historical data for the defined date range
nifty_data = yf.download(ticker_symbol, start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'), interval="1d")

# Extract the closing prices
closing_prices = nifty_data['Close']

# Define expiry date
Expiry_Date = datetime(2024, 11, 7)

# Calculate number of days to expiry date and store as float
DTE = float((Expiry_Date - datetime.today()).days)

# Check if closing prices were fetched
if closing_prices.empty:
    print("No data fetched for the specified ticker and date range.")
else:
    # Calculate the daily percentage change
    percentage_change = closing_prices.pct_change() * 100  # Multiply by 100 to get the percentage

    # Calculate the standard deviation of the daily percentage change
    Daily_Volatility = percentage_change.std()

    # Calculate Standard Deviation as Daily_Volatility * sqrt(DTE)
    Standard_Deviation = Daily_Volatility * math.sqrt(DTE)

    # Calculate the average closing price of the last 2 available dates
    Average_Closing_Price = closing_prices.tail(2).mean()

    # Get the last closing price
    Last_Closing_Price = closing_prices.iloc[-1]

    # Calculate Abs_Stdev as Standard_Deviation * Last_Closing_Price
    Abs_Stdev = Standard_Deviation * Last_Closing_Price

    # Calculate the Z-score as a float
    Z_Score = float((Last_Closing_Price - Average_Closing_Price) / Abs_Stdev)

    # Calculate Probability using the CDF of the standard normal distribution
    Probability = 1- norm.cdf(Z_Score)  # Using mean=0 and std=1 by default

    # Determine the trend based on Z-score
    if Z_Score < 0:
        trend = "Bearish"
    else:
        trend = "Bullish"

    # Print the closing prices, daily percentage change, daily volatility, expiry date, DTE, standard deviation, average closing price, Z-score, Abs_Stdev, probability, and trend
    print("Closing Prices:")
    print(closing_prices)

    print("\nDaily Percentage Change:")
    print(percentage_change)

    print("\nDaily Volatility (Standard Deviation of Daily % Change):", Daily_Volatility)

    print("\nExpiry Date:", Expiry_Date.strftime('%Y-%m-%d'))
    print("Days to Expiry (DTE):", DTE)

    print("Standard Deviation (Daily Volatility * sqrt(DTE)):", Standard_Deviation)

    print("Average Closing Price of the Last 2 Days:", Average_Closing_Price)

    print("Last Closing Price:", Last_Closing_Price)

    print("Z-Score:", Z_Score)

    print("Absolute Standard Deviation (Abs_Stdev):", Abs_Stdev)

    print("Probability (using standard normal CDF):", Probability)  # Print the calculated probability

    print("Trend:", trend)  # Print the trend