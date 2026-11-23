from datetime import datetime, timezone

class TickGuard:
    def __init__(self, max_age_seconds=10):
        self.max_age=max_age_seconds
        self.last={}
        self.seen=set()

    def check(self, symbol, tick, now=None):
        now = now if now is not None else datetime.now(timezone.utc).timestamp()
        price, ts = tick.get("price"), tick.get("timestamp")
        if not isinstance(price,(int,float)) or price<=0: return False,"invalid_price"
        if not isinstance(ts,(int,float)): return False,"invalid_timestamp"
        age=now-ts
        if age < -2: return False,"future_timestamp"
        if age > self.max_age: return False,"stale_tick"
        key=(symbol,ts,price)
        if key in self.seen: return False,"duplicate_tick"
        if ts < self.last.get(symbol,0): return False,"out_of_order_tick"
        self.seen.add(key); self.last[symbol]=ts
        if len(self.seen)>10000: self.seen.clear()
        return True,"good"
