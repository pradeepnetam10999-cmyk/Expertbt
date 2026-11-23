# Roadmap and honest completion status

Included: dashboard shell, API, database tables, 20-module registry, deterministic baseline experts, fusion, WAIT gate, virtual demo account, demo trade settlement endpoint, signal ledger, provider adapter classes, key settings, simple backtest and learning metrics.

Still required before production:
1. Auth, roles, per-user data isolation and audit.
2. Persistent Finnhub stream manager, subscription lifecycle and frontend live event delivery.
3. Broker-authorized OTC feed and independent OTC dataset.
4. News calendar and multi-timeframe aggregation.
5. Persistent candle archive and automatic expiry outcome reconciliation.
6. Execution-realistic backtesting with payout schedules, latency, spreads and missing data.
7. Probability calibration, confidence intervals and model registry.
8. Alembic migrations, rate limits, monitoring, backups and security review.
9. Deployment, HTTPS and operational runbooks.

No real-money execution is included.
