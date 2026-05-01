import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns

# =============================================
# PAGE SETTINGS
# =============================================

st.set_page_config(
    page_title="Goutam Dukka | Portfolio Analyzer",
    page_icon="📈",
    layout="wide"
)

# =============================================
# CUSTOM CSS
# =============================================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Roboto+Mono:wght@300;400;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Roboto Mono', monospace;
    }

    .header-banner {
        background: linear-gradient(135deg, #0D0D0D 0%, #1a1a2e 50%, #0D0D0D 100%);
        border: 1px solid #00FF41;
        border-radius: 8px;
        padding: 30px 40px;
        margin-bottom: 30px;
        text-align: center;
    }

    .header-logo {
        font-family: 'Share Tech Mono', monospace;
        font-size: 48px;
        font-weight: 700;
        color: #00FF41;
        letter-spacing: 4px;
        margin-bottom: 4px;
    }

    .header-name {
        font-size: 20px;
        color: #E0E0E0;
        letter-spacing: 2px;
        margin-bottom: 6px;
    }

    .header-tagline {
        font-size: 13px;
        color: #888888;
        letter-spacing: 3px;
        text-transform: uppercase;
    }

    .header-divider {
        border: none;
        border-top: 1px solid #00FF41;
        margin: 16px auto;
        width: 60%;
        opacity: 0.4;
    }

    .metric-box {
        background-color: #1A1A1A;
        border: 1px solid #00FF41;
        border-radius: 6px;
        padding: 16px;
        text-align: center;
        margin-bottom: 10px;
    }

    .metric-label {
        font-size: 11px;
        color: #888888;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 6px;
    }

    .metric-value {
        font-size: 24px;
        font-weight: 700;
        color: #00FF41;
    }

    .section-title {
        font-family: 'Share Tech Mono', monospace;
        font-size: 16px;
        color: #00FF41;
        letter-spacing: 3px;
        text-transform: uppercase;
        border-bottom: 1px solid #333;
        padding-bottom: 8px;
        margin: 30px 0 16px 0;
    }

    .stButton>button {
        background-color: #00FF41;
        color: #0D0D0D;
        font-family: 'Roboto Mono', monospace;
        font-weight: 700;
        letter-spacing: 2px;
        border: none;
        width: 100%;
        padding: 12px;
        border-radius: 4px;
    }

    .stButton>button:hover {
        background-color: #00cc33;
        color: #0D0D0D;
    }

    footer {
        text-align: center;
        color: #444;
        font-size: 11px;
        margin-top: 60px;
        letter-spacing: 2px;
    }
</style>
""", unsafe_allow_html=True)

# =============================================
# HEADER BANNER
# =============================================

st.markdown("""
<div class="header-banner">
    <div class="header-logo">[ PORTFOLIO ANALYZER ]</div>
    <hr class="header-divider">
    <div class="header-name">GOUTAM DUKKA</div>
    <div class="header-tagline">Aspiring Asset Management Professional</div>
</div>
""", unsafe_allow_html=True)

# =============================================
# SIDEBAR
# =============================================

st.sidebar.markdown("### ⚙️ PORTFOLIO SETTINGS")

default_tickers = "RELIANCE.NS, TCS.NS, HDFCBANK.NS, INFY.NS, ITC.NS"
default_names = "Reliance, TCS, HDFC Bank, Infosys, ITC"

ticker_input = st.sidebar.text_area("NSE Tickers (comma separated)", default_tickers)
names_input = st.sidebar.text_area("Stock Names (comma separated)", default_names)
start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime("2020-01-01"))
end_date = st.sidebar.date_input("End Date", value=pd.to_datetime("2024-12-31"))
run = st.sidebar.button("▶ RUN ANALYSIS")

st.sidebar.markdown("---")
st.sidebar.markdown("**Common NSE Tickers:**")
st.sidebar.markdown("""
`WIPRO.NS` · `BAJFINANCE.NS`  
`MARUTI.NS` · `LT.NS`  
`SBIN.NS` · `ICICIBANK.NS`  
`KOTAKBANK.NS` · `HINDUNILVR.NS`
""")

# =============================================
# CHART STYLE
# =============================================

def set_dark_style():
    mpl.rcParams.update({
        "figure.facecolor": "#0D0D0D",
        "axes.facecolor": "#1A1A1A",
        "axes.edgecolor": "#333333",
        "axes.labelcolor": "#888888",
        "xtick.color": "#888888",
        "ytick.color": "#888888",
        "grid.color": "#2a2a2a",
        "text.color": "#E0E0E0",
        "legend.facecolor": "#1A1A1A",
        "legend.edgecolor": "#333333",
        "font.family": "monospace",
    })

COLORS = ["#00FF41", "#00BFFF", "#FF6B6B", "#FFD700", "#CC00FF"]

# =============================================
# MAIN APP
# =============================================

if run:
    tickers = [t.strip() for t in ticker_input.split(",")]
    names = [n.strip() for n in names_input.split(",")]

    with st.spinner("[ FETCHING MARKET DATA... ]"):
        data = yf.download(tickers, start=start_date, end=end_date)["Close"]
        nifty = yf.download("^NSEI", start=start_date, end=end_date)["Close"]

    st.success("✅ Data loaded successfully")

    returns = data.pct_change().dropna()
    nifty_returns = nifty.pct_change().dropna()
    ann_return = returns.mean() * 252
    ann_vol = returns.std() * (252 ** 0.5)
    sharpe = ann_return / ann_vol
    cumulative = (1 + returns).cumprod()
    rolling_max = cumulative.cummax()
    drawdown = (cumulative - rolling_max) / rolling_max
    max_drawdown = drawdown.min()
    nifty_cum = (1 + nifty_returns).cumprod()

    # METRICS ROW
    st.markdown('<div class="section-title">// PORTFOLIO METRICS</div>', unsafe_allow_html=True)
    cols = st.columns(len(tickers))
    for i, (ticker, name) in enumerate(zip(tickers, names)):
        with cols[i]:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-label">{name}</div>
                <div class="metric-value">{ann_return[ticker]:.1%}</div>
                <div class="metric-label">annual return</div>
                <br>
                <div style="color:#888;font-size:12px;">Sharpe: <span style="color:#00FF41">{sharpe[ticker]:.2f}</span></div>
                <div style="color:#888;font-size:12px;">Max DD: <span style="color:#FF6B6B">{max_drawdown[ticker]:.1%}</span></div>
                <div style="color:#888;font-size:12px;">Vol: <span style="color:#FFD700">{ann_vol[ticker]:.1%}</span></div>
            </div>
            """, unsafe_allow_html=True)

    set_dark_style()

    # CHART 1 — CUMULATIVE RETURNS
    st.markdown('<div class="section-title">// CUMULATIVE RETURNS VS NIFTY 50</div>', unsafe_allow_html=True)
    fig1, ax1 = plt.subplots(figsize=(13, 5))
    for i, (ticker, name) in enumerate(zip(tickers, names)):
        ax1.plot(cumulative[ticker], label=name, color=COLORS[i % len(COLORS)], linewidth=1.5)
    ax1.plot(nifty_cum, label="Nifty 50", color="white", linewidth=2, linestyle="--", alpha=0.6)
    ax1.set_ylabel("Growth of ₹1")
    ax1.legend(fontsize=9)
    ax1.grid(True, alpha=0.2)
    plt.tight_layout()
    st.pyplot(fig1)

    # CHART 2 — DRAWDOWN
    st.markdown('<div class="section-title">// DRAWDOWN CHART</div>', unsafe_allow_html=True)
    fig2, ax2 = plt.subplots(figsize=(13, 4))
    for i, (ticker, name) in enumerate(zip(tickers, names)):
        ax2.plot(drawdown[ticker], label=name, color=COLORS[i % len(COLORS)], linewidth=1.2)
    ax2.fill_between(drawdown.index, drawdown.min(axis=1), alpha=0.15, color="#FF6B6B")
    ax2.set_ylabel("Drawdown")
    ax2.legend(fontsize=9)
    ax2.grid(True, alpha=0.2)
    plt.tight_layout()
    st.pyplot(fig2)

    # CHART 3 — CORRELATION
    st.markdown('<div class="section-title">// CORRELATION MATRIX</div>', unsafe_allow_html=True)
    corr = returns.copy()
    corr.columns = names
    fig3, ax3 = plt.subplots(figsize=(8, 5))
    sns.heatmap(corr.corr(), annot=True, cmap="RdYlGn", fmt=".2f", ax=ax3,
                linewidths=0.5, linecolor="#0D0D0D")
    ax3.set_facecolor("#1A1A1A")
    fig3.patch.set_facecolor("#0D0D0D")
    plt.tight_layout()
    st.pyplot(fig3)

    # EFFICIENT FRONTIER
    st.markdown('<div class="section-title">// EFFICIENT FRONTIER</div>', unsafe_allow_html=True)
    num_portfolios = 3000
    results = np.zeros((3, num_portfolios))
    weights_record = []
    for i in range(num_portfolios):
        weights = np.random.random(len(tickers))
        weights /= np.sum(weights)
        weights_record.append(weights)
        port_return = np.sum(returns.mean() * weights) * 252
        port_vol = np.sqrt(np.dot(weights.T, np.dot(returns.cov() * 252, weights)))
        results[0, i] = port_return
        results[1, i] = port_vol
        results[2, i] = port_return / port_vol

    fig4, ax4 = plt.subplots(figsize=(11, 6))
    sc = ax4.scatter(results[1], results[0], c=results[2], cmap="plasma", alpha=0.6, s=8)
    plt.colorbar(sc, ax=ax4, label="Sharpe Ratio")
    ax4.set_xlabel("Annualised Volatility")
    ax4.set_ylabel("Annualised Return")
    ax4.grid(True, alpha=0.2)
    plt.tight_layout()
    st.pyplot(fig4)

    best_idx = np.argmax(results[2])
    best_weights = weights_record[best_idx]
    st.markdown('<div class="section-title">// OPTIMAL PORTFOLIO WEIGHTS</div>', unsafe_allow_html=True)
    opt_cols = st.columns(len(tickers))
    for i, (name, w) in enumerate(zip(names, best_weights)):
        with opt_cols[i]:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-label">{name}</div>
                <div class="metric-value">{w:.1%}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<footer>GOUTAM DUKKA · PORTFOLIO ANALYZER · BUILT WITH PYTHON & STREAMLIT</footer>",
                unsafe_allow_html=True)

else:
    st.markdown('<div class="section-title">// HOW TO USE</div>', unsafe_allow_html=True)
    st.markdown("""1. Enter NSE stock tickers in the sidebar (e.g. RELIANCE.NS)
2. Enter the corresponding stock names
3. Select your date range
4. Click RUN ANALYSIS""")
    st.info("👈 Configure your portfolio in the sidebar to get started")