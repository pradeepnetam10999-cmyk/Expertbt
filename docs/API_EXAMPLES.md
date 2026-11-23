# API examples

GET /api/health
GET /api/brain/modules
GET /api/signals
GET /api/demo/account

POST /api/brain/evaluate
```json
{
  "symbol":"EUR/USD",
  "market_type":"NON_OTC",
  "timeframe":"1min",
  "expiry_seconds":60,
  "profile":"BALANCED",
  "data_quality":"GOOD",
  "candles":[
    {"timestamp":1700000000,"open":1.08,"high":1.081,"low":1.079,"close":1.0805,"volume":0}
  ]
}
```
Supply at least 25 chronological candles for baseline experts.

POST /api/demo/trades
```json
{"symbol":"EUR/USD","direction":"CALL","stake":10,"payout_rate":0.8,"entry_price":1.08,"expiry_seconds":60}
```

POST /api/demo/trades/{id}/settle?expiry_price=1.081
Settlement is a demo-only endpoint and trusts the supplied price; do not use it for real orders.
