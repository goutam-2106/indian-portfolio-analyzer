import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# =============================================
# INDIAN LARGE CAP PORTFOLIO ANALYZER
# Reliance, TCS, HDFC Bank, Infosys, ITC
# Benchmarked against Nifty 50
# =============================================

tickers = ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "ITC.NS"]
benchmark = "^NSEI"
names = ["Reliance", "TCS", "HDFC Bank", "Infosys", "ITC"]

print("Downloading data from NSE... please wait")
data = yf.download(tickers, start="2020-01-01", end="2024-12-31")["Close"]
nifty = yf.download(benchmark, start="2020-01-01", end="2024-12-31")["Close"]
print("Done!\n")

# =============================================
# RETURNS & RISK METRICS
# =============================================

returns = data.pct_change().dropna()
nifty_returns = nifty.pct_change().dropna()

ann_return = returns.mean() * 252
ann_vol = returns.std() * (252 ** 0.5)
sharpe = ann_return / ann_vol

cumulative = (1 + returns).cumprod()
rolling_max = cumulative.cummax()
drawdown = (cumulative - rolling_max) / rolling_max
max_drawdown = drawdown.min()

print("=" * 45)
print("        PORTFOLIO METRICS SUMMARY")
print("=" * 45)
print(f"\n{'Stock':<12} {'Return':>10} {'Volatility':>12} {'Sharpe':>8} {'Max DD':>10}")
print("-" * 55)
for i, name in enumerate(names):
    ticker = tickers[i]
    print(f"{name:<12} {ann_return[ticker]:>9.1%} {ann_vol[ticker]:>11.1%} {sharpe[ticker]:>8.2f} {max_drawdown[ticker]:>9.1%}")

# =============================================
# CHART 1 — CUMULATIVE RETURNS vs NIFTY 50
# =============================================

nifty_cum = (1 + nifty_returns).cumprod()

plt.figure(figsize=(13, 6))
for ticker, name in zip(tickers, names):
    plt.plot(cumulative[ticker], label=name, linewidth=1.5)
plt.plot(nifty_cum, label="Nifty 50 (Benchmark)", color="black", linewidth=2, linestyle="--")
plt.title("Cumulative Returns vs Nifty 50 (2020–2024)", fontsize=14)
plt.ylabel("Growth of ₹1")
plt.xlabel("Date")
plt.legend()
plt.tight_layout()
plt.show()

# =============================================
# CHART 2 — CORRELATION HEATMAP
# =============================================

plt.figure(figsize=(8, 6))
corr = returns.copy()
corr.columns = names
sns.heatmap(corr.corr(), annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Between Stocks\n(1.0 = move together, -1.0 = move opposite)", fontsize=13)
plt.tight_layout()
plt.show()

# =============================================
# CHART 3 — DRAWDOWN CHART
# =============================================

plt.figure(figsize=(13, 5))
for ticker, name in zip(tickers, names):
    plt.plot(drawdown[ticker], label=name, linewidth=1.2)
plt.fill_between(drawdown.index, drawdown.min(axis=1), alpha=0.1, color="red")
plt.title("Drawdown Chart — How Far Each Stock Fell From Its Peak", fontsize=14)
plt.ylabel("Drawdown (%)")
plt.xlabel("Date")
plt.legend()
plt.tight_layout()
plt.show()

print("\nAll charts displayed successfully!")
print("You can now see how each stock performed vs the Nifty 50 benchmark.")