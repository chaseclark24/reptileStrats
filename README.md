# Reptile Strategies

A set of Python experiments for automating cryptocurrency strategy backtests through a local [Gekko](https://github.com/askmike/gekko) trading-bot API.

> **Status:** Historical research code. Gekko is no longer actively maintained, and these scripts contain local paths and assumptions from the original workstation.

## What the scripts explored

The scripts generated randomized strategy parameters, submitted backtest requests to a local Gekko server, and wrote performance statistics for later comparison.

Strategies and indicators include:

- MACD
- DEMA
- Stochastic RSI
- Multi-process and repeated-test variants

The captured results included profitability, trade count, exposure, Sharpe ratio, alpha, and the parameter combination used for each run.

## Technology

- Python
- Gekko's local REST API
- `requests`
- Python multiprocessing

## Repository limitations

- Paths and date ranges are hard-coded.
- Several scripts run indefinitely until manually stopped.
- Output files and the Gekko installation are not included.
- The scripts were exploratory rather than a packaged trading system.

This code should not be treated as financial advice or as a production trading strategy.
