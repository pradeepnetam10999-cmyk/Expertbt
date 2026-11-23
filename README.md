# Binary Trading Expert | Full-Scale Research & Demo WebApp

A modular React + TypeScript + FastAPI project for binary-options market research, expert-signal evaluation, virtual trades, replay foundations and learning research.

## Included
- Responsive multi-page trading dashboard with candlestick chart
- FastAPI backend, SQLAlchemy persistence, SQLite default and PostgreSQL option
- Twenty named expert departments and baseline deterministic evaluators
- Expert fusion engine with Conservative / Balanced / Active profiles
- CALL / PUT / WAIT, with WAIT as a first-class safety outcome
- Tick quality guard, duplicate/out-of-order/stale checks and candle builder
- Finnhub reconnecting WebSocket adapter class
- Twelve Data historical-candle adapter
- Server-side API-key settings endpoint
- OTC/non-OTC separation; OTC intentionally gated without authorized broker feed
- Demo account, virtual trade lifecycle, signal ledger, simple backtest and learning metrics
- Tests, Docker files, environment examples, architecture/security documentation

## Important
This is a research/demo codebase, not a guaranteed-profit product or broker execution terminal. It does not place real-money trades. API access requires your own provider credentials and plan entitlements. A regular FX feed is not an OTC broker feed. The OTC engine returns WAIT until a documented authorized OTC feed exists. Strength scores are not calibrated win probabilities. No martingale or loss-chasing logic is implemented.

## Run backend
```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\Activate.ps1
# Linux/macOS/Termux:
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
API docs: http://localhost:8000/docs

## Run frontend (second terminal)
```bash
cd frontend
npm install
npm run dev -- --host 0.0.0.0
```
Open http://localhost:5173

## Optional PostgreSQL
```bash
docker compose up -d db
```
Then set DATABASE_URL in backend/.env. SQLite works by default.

## Provider keys
Use Data Providers in the app. Keys are sent to the backend and written to backend/.env. Never commit .env. Restart the backend after saving. Production should use a secrets manager/encrypted credential service and authentication.

## Before production
Add authentication, authorization, per-user isolation, HTTPS, rate limits, secret vault, migrations, monitoring, backups, realistic execution-aware backtests, provider reconciliation, validated OTC adapter, statistical calibration, independent security review and legal/platform compliance review.
