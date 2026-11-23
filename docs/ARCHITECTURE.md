# All-Learning Architecture

## Data plane
Provider adapters -> normalized events -> stale/duplicate/order checks -> candle construction -> immutable closed candles -> experts.

## Decision plane
20 experts -> weighted consensus -> data-quality/conflict/risk gates -> frequency profile -> CALL/PUT/WAIT -> immutable signal snapshot.

## Learning plane
Outcome reconciliation -> chronological dataset -> walk-forward validation -> calibration and confidence intervals -> challenger/champion comparison -> reviewed model version -> rollback monitoring.

## Expert departments
1 Market structure; 2 Candlesticks; 3 Price action; 4 Indicators; 5 Expiry intelligence; 6 Entry timing; 7 Volatility; 8 Multi-timeframe; 9 Market psychology proxies; 10 Sessions; 11 OTC intelligence; 12 News; 13 Probability; 14 Strategy; 15 Confirmation; 16 Risk; 17 Data quality; 18 Learning; 19 Signal intelligence; 20 Self-monitoring.

The first seven have baseline deterministic heuristics. Other departments expose explicit neutral/context/safety outputs where data or validated models are not supplied. Listed modules are not all trained AI models.

## Frequency profiles
Conservative/Balanced/Active alter thresholds, never target counts. Data quality and risk gates override every profile. Balanced is default.

## Market separation
OTC and non-OTC must have separate feeds, data lineage, backtests and performance reports. Ordinary market data is not a broker OTC proxy.

## Anti-leakage
Use chronological train/validation/test splits and walk-forward testing. Do not random-shuffle time series or use future candle values. Track payout, spread, latency, ties, missing data and sample size.
