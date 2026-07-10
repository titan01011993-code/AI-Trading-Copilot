# 🚀 AI Trading Copilot

A production-grade AI-powered algorithmic trading platform for the Indian stock market.

> **Status:** 🚧 Under Active Development (Sprint-1)

---

# Features

## Market Data

- Multi-timeframe historical data
- Yahoo Finance Provider
- Dhan Broker (Upcoming)
- Angel One (Upcoming)
- Data validation
- Candle cleaning
- Timeframe normalization

Supported Timeframes

- 5m
- 15m
- 30m
- 1H
- 4H
- 1D
- 1W
- 1M

---

# Technical Indicators

Implemented

- EMA 20
- EMA 50
- EMA 200
- RSI
- MACD
- ATR
- ADX
- VWAP
- SuperTrend

---

# Smart Money Concepts

Implemented

- Swing High
- Swing Low
- Break Of Structure (BOS)
- Change Of Character (CHOCH)
- Order Blocks
- Fair Value Gaps (FVG)
- Liquidity Zones
- Liquidity Sweep
- Mitigation

---

# AI Feature Engine

Implemented

- Trend Features
- Momentum Features
- Volume Features
- Volatility Features
- Smart Money Features

---

# AI Decision Engine

Current Development

- Technical Score
- Market Bias
- Confidence
- Buy Score
- Sell Score
- Hold Score

---

# Trade Engine

Upcoming

- Entry
- Stop Loss
- Target 1
- Target 2
- Risk Reward
- Position Size

---

# Risk Management

Upcoming

- ATR Risk
- Fixed Risk %
- Dynamic Position Sizing
- Daily Loss Limit
- Portfolio Risk

---

# Multi-Timeframe Analysis

Upcoming

Daily

↓

4H

↓

1H

↓

15m

↓

5m

---

# Backtesting

Upcoming

- Historical Replay
- Win Rate
- Profit Factor
- Max Drawdown
- Expectancy
- Equity Curve

---

# Live Trading

Upcoming

- Dhan API
- Angel One API
- Order Placement
- Position Management
- Auto Exit

---

# Dashboard

Upcoming

- Streamlit
- Live Chart
- Scanner
- Trade Journal
- Portfolio

---

# Project Structure

```
AI-Trading-Copilot/

├── core/
├── market/
├── indicators/
├── features/
├── engine/
├── strategy/
├── execution/
├── broker/
├── scanner/
├── portfolio/
├── dashboard/
├── tests/
├── config/
├── utils/
└── docs/
```

---

# Development Roadmap

## Sprint 1

- [x] Market Data
- [x] Indicators
- [x] Smart Money
- [x] Feature Engine
- [x] Technical Engine
- [ ] Decision Engine
- [ ] Trade Planner
- [ ] Risk Engine
- [ ] Signal Engine
- [ ] Confidence Engine

---

## Sprint 2

- [ ] Multi-Timeframe Engine
- [ ] Strategy Engine
- [ ] Market Scanner

---

## Sprint 3

- [ ] Backtesting
- [ ] Optimization
- [ ] Trade Analytics

---

## Sprint 4

- [ ] Dhan Integration
- [ ] Paper Trading
- [ ] Live Trading

---

## Sprint 5

- [ ] Dashboard
- [ ] Telegram Alerts
- [ ] Portfolio Analytics

---

# Installation

Clone repository

```bash
git clone https://github.com/YOUR_USERNAME/AI-Trading-Copilot.git

cd AI-Trading-Copilot
```

Create virtual environment

```bash
python -m venv .venv
```

Activate

Windows

```bash
.venv\Scripts\activate
```

Linux / Mac

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# Run Tests

```bash
python -m tests.test_history

python -m tests.test_pipeline

python -m tests.test_features

python -m tests.test_technical_engine
```

---

# Tech Stack

- Python 3.13
- Pandas
- NumPy
- yfinance
- Plotly
- Streamlit
- DhanHQ
- Angel One
- Git
- GitHub

---

# Coding Standards

- Production-ready code only
- Type hints
- Unit tests
- No placeholder code
- Backward compatible updates
- Modular architecture

---

# Git Workflow

```bash
git checkout -b feature/module-name

git add .

git commit -m "feat: module"

git push origin feature/module-name
```

---

# Current Progress

Overall Progress

**45% Complete**

Architecture

**90% Complete**

Production Readiness

**35% Complete**

---

# License

MIT License

---

# Author

**Sachin**

AI Trading Copilot Project
