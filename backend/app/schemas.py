from typing import Literal
from pydantic import BaseModel, Field

class Candle(BaseModel):
    timestamp: int
    open: float
    high: float
    low: float
    close: float
    volume: float = 0

class EvaluateRequest(BaseModel):
    symbol: str
    market_type: Literal["OTC", "NON_OTC"] = "NON_OTC"
    timeframe: str = "1min"
    expiry_seconds: int = Field(default=60, gt=0, le=3600)
    profile: Literal["CONSERVATIVE", "BALANCED", "ACTIVE"] = "BALANCED"
    data_quality: Literal["GOOD", "DEGRADED", "INVALID"] = "GOOD"
    candles: list[Candle] = Field(default_factory=list)

class DemoTradeRequest(BaseModel):
    symbol: str
    direction: Literal["CALL", "PUT"]
    stake: float = Field(gt=0, le=100000)
    payout_rate: float = Field(default=.8, ge=0, le=1)
    entry_price: float = Field(gt=0)
    expiry_seconds: int = Field(gt=0, le=3600)

class ProviderKeyRequest(BaseModel):
    provider: Literal["finnhub", "twelve_data"]
    api_key: str = Field(min_length=5, max_length=300)
