from datetime import datetime, timezone
from sqlalchemy import String, Float, Integer, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base

def now_utc():
    return datetime.now(timezone.utc)

class SignalRecord(Base):
    __tablename__ = "signals"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_utc)
    symbol: Mapped[str] = mapped_column(String(80), index=True)
    market_type: Mapped[str] = mapped_column(String(20), index=True)
    timeframe: Mapped[str] = mapped_column(String(20))
    expiry_seconds: Mapped[int] = mapped_column(Integer)
    decision: Mapped[str] = mapped_column(String(12))
    tier: Mapped[str] = mapped_column(String(20))
    strength_score: Mapped[float] = mapped_column(Float, default=0)
    agreement: Mapped[float] = mapped_column(Float, default=0)
    outcome: Mapped[str] = mapped_column(String(20), default="PENDING")
    explanation: Mapped[str] = mapped_column(Text, default="")
    snapshot_json: Mapped[str] = mapped_column(Text, default="{}")

class DemoAccount(Base):
    __tablename__ = "demo_accounts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    balance: Mapped[float] = mapped_column(Float, default=10000)
    initial_balance: Mapped[float] = mapped_column(Float, default=10000)

class DemoTrade(Base):
    __tablename__ = "demo_trades"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_utc)
    symbol: Mapped[str] = mapped_column(String(80))
    direction: Mapped[str] = mapped_column(String(8))
    stake: Mapped[float] = mapped_column(Float)
    payout_rate: Mapped[float] = mapped_column(Float)
    entry_price: Mapped[float] = mapped_column(Float)
    expiry_seconds: Mapped[int] = mapped_column(Integer)
    expiry_price: Mapped[float | None] = mapped_column(Float, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="OPEN")
    pnl: Mapped[float] = mapped_column(Float, default=0)
