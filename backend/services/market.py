from app.brain.quality import TickGuard
from app.brain.candles import CandleBuilder
from app.core.config import settings

class MarketState:
    def __init__(self):
        self.guard=TickGuard(settings.max_tick_age_seconds)
        self.builders={60:CandleBuilder(60),300:CandleBuilder(300),900:CandleBuilder(900)}
        self.latest={}; self.status={"state":"DEMO","connected":False}
    def ingest(self,tick):
        symbol=tick["symbol"]; ok,reason=self.guard.check(symbol,tick)
        if not ok: return {"accepted":False,"reason":reason}
        self.latest[symbol]=tick; closed={}
        for interval,builder in self.builders.items():
            candle=builder.ingest(symbol,int(tick["timestamp"]),tick["price"],tick.get("volume",0))
            if candle: closed[str(interval)]=candle
        return {"accepted":True,"completed_candles":closed}
