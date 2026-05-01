# 📈 Indian Large Cap Portfolio Analyzer

A Python-based portfolio analytics tool that pulls **real market data** from NSE-listed stocks and generates a comprehensive risk and performance report — benchmarked against the **Nifty 50**.

---

## 🔍 What It Does

- Downloads historical price data for Indian large cap stocks using Yahoo Finance
- Calculates key risk-adjusted performance metrics for each stock
- Benchmarks portfolio performance against the Nifty 50 index
- Generates three professional visualisations

---

## 📊 Metrics Calculated

| Metric | Description |
|---|---|
| **Annualised Return** | Average yearly return for each stock |
| **Annualised Volatility** | How much the price fluctuates per year |
| **Sharpe Ratio** | Return earned per unit of risk taken |
| **Max Drawdown** | Worst peak-to-trough loss over the period |

---

## 📉 Charts Generated

1. **Cumulative Returns vs Nifty 50** — Shows growth of ₹1 invested in January 2020 across all stocks, benchmarked against the index
2. **Correlation Heatmap** — Shows how stocks move relative to each other, useful for understanding diversification
3. **Drawdown Chart** — Visualises the depth and duration of losses from peak values for each stock

---

## 🏦 Portfolio

| Stock | Ticker |
|---|---|
| Reliance Industries | RELIANCE.NS |
| Tata Consultancy Services | TCS.NS |
| HDFC Bank | HDFCBANK.NS |
| Infosys | INFY.NS |
| ITC | ITC.NS |
| Nifty 50 (Benchmark) | ^NSEI |

**Period:** January 2020 – December 2024

---

## 🛠️ Technologies Used

- **Python** — core programming language
- **yfinance** — real-time and historical market data from Yahoo Finance
- **pandas** — data manipulation and time series analysis
- **numpy** — numerical computations and financial math
- **matplotlib** — chart generation
- **seaborn** — correlation heatmap visualisation

---

## 🚀 How To Run

**1. Clone the repository**
```
git clone https://github.com/goutam-2106/indian-portfolio-analyzer.git
cd indian-portfolio-analyzer
```

**2. Install dependencies**
```
pip install yfinance pandas numpy matplotlib seaborn
```

**3. Run the analyzer**
```
python portfolio.py
```

---

## 💡 Key Concepts

**Sharpe Ratio** — measures return relative to risk. A ratio above 1.0 is considered good. It answers: "Was the return worth the volatility?"

**Max Drawdown** — the largest drop from a peak before a recovery. Critical for understanding downside risk in a portfolio.

**Correlation** — if two stocks are highly correlated, they tend to fall together. A well-diversified portfolio has stocks with low correlation to each other.

---

## 👤 Author

**Goutam** — MBA in Finance | Aspiring Asset Management Professional

---

*Built to demonstrate practical application of Python in financial analysis and portfolio management.*
