import httpx,datetime
from app.core.config import settings

class TwelveData:
    async def candles(self,symbol,interval="1min",outputsize=300):
        if not settings.twelve_data_api_key: raise RuntimeError("Twelve Data API key not configured")
        params={"symbol":symbol,"interval":interval,"outputsize":outputsize,
                "apikey":settings.twelve_data_api_key,"format":"JSON"}
        async with httpx.AsyncClient(timeout=20) as client:
            response=await client.get("https://api.twelvedata.com/time_series",params=params)
            response.raise_for_status(); data=response.json()
        if "values" not in data: raise RuntimeError(data.get("message","No candle values returned"))
        rows=[]
        for x in reversed(data["values"]):
            dt=datetime.datetime.fromisoformat(x["datetime"])
            rows.append({"timestamp":int(dt.timestamp()),"open":float(x["open"]),
                "high":float(x["high"]),"low":float(x["low"]),"close":float(x["close"]),
                "volume":float(x.get("volume") or 0)})
        return rows
