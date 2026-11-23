import asyncio,json,websockets
from app.core.config import settings

class FinnhubStream:
    def __init__(self,symbols,on_tick,on_status=None):
        self.symbols=symbols; self.on_tick=on_tick; self.on_status=on_status or (lambda x:None)
        self.stop_event=asyncio.Event()
    async def stop(self): self.stop_event.set()
    async def run(self):
        if not settings.finnhub_api_key:
            self.on_status({"state":"NOT_CONFIGURED"}); return
        delay=1
        while not self.stop_event.is_set():
            try:
                async with websockets.connect(f"wss://ws.finnhub.io?token={settings.finnhub_api_key}",
                    ping_interval=20,ping_timeout=20) as ws:
                    for symbol in self.symbols:
                        await ws.send(json.dumps({"type":"subscribe","symbol":symbol}))
                    self.on_status({"state":"CONNECTED","symbols":self.symbols}); delay=1
                    async for raw in ws:
                        payload=json.loads(raw)
                        if payload.get("type")=="trade":
                            for t in payload.get("data",[]):
                                await self.on_tick({"symbol":t["s"],"price":float(t["p"]),
                                    "timestamp":int(t["t"])/1000,"volume":float(t.get("v",0))})
            except asyncio.CancelledError: raise
            except Exception as exc:
                self.on_status({"state":"RECONNECTING","error":str(exc)[:160],"retry_seconds":delay})
                await asyncio.sleep(delay); delay=min(delay*2,60)
