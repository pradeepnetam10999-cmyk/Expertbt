class CandleBuilder:
    def __init__(self, interval_seconds=60):
        self.interval=interval_seconds
        self.current={}

    def ingest(self,symbol,timestamp,price,volume=0):
        bucket=timestamp-(timestamp%self.interval)
        c=self.current.get(symbol)
        if c is None or c["timestamp"]!=bucket:
            completed=c
            self.current[symbol]={"timestamp":bucket,"open":price,"high":price,
                "low":price,"close":price,"volume":volume}
            return completed
        c["high"]=max(c["high"],price); c["low"]=min(c["low"],price)
        c["close"]=price; c["volume"]+=volume
        return None

    def snapshot(self,symbol):
        c=self.current.get(symbol)
        return dict(c) if c else None
