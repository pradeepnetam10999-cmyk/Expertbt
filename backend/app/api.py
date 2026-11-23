import json
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.config import settings
from app.core.secrets import store_provider_key
from app.schemas import EvaluateRequest,DemoTradeRequest,ProviderKeyRequest
from app.models.tables import SignalRecord,DemoTrade
from app.services.signals import evaluate
from app.services.demo import get_account,create_trade,settle
from app.providers.twelve_data import TwelveData
from app.brain.learning import summarize,expected_value

router=APIRouter()

@router.get("/health")
def health():
    return {"status":"ok","mode":"research_demo","real_money_execution":False}

@router.get("/brain/modules")
def modules():
    names=["Market Structure","Candlestick Expert","Price Action","Indicator Expert","Expiry Intelligence",
    "Entry Timing","Volatility Expert","Multi-Timeframe","Market Psychology","Session Intelligence",
    "OTC Intelligence","News Intelligence","Probability Expert","Strategy Expert","Confirmation Expert",
    "Risk Intelligence","Data Intelligence","Learning Engine","Signal Intelligence","Self-Monitoring"]
    return {"architecture":"ALL_LEARNING","modules":[{"name":n,"status":"FOUNDATION"} for n in names]}

@router.post("/brain/evaluate")
def brain(payload:EvaluateRequest,db:Session=Depends(get_db)):
    try: return evaluate(db,payload.model_dump())
    except Exception as e: raise HTTPException(400,str(e))

@router.get("/market/candles")
async def candles(symbol:str,interval:str="1min",outputsize:int=200):
    try: return {"symbol":symbol,"candles":await TwelveData().candles(symbol,interval,min(outputsize,5000))}
    except Exception as e: raise HTTPException(400,str(e))

@router.post("/settings/provider-key")
def provider_key(payload:ProviderKeyRequest):
    try: return store_provider_key(payload.provider,payload.api_key)
    except Exception as e: raise HTTPException(400,str(e))

@router.get("/settings/providers")
def providers():
    return {"finnhub_configured":bool(settings.finnhub_api_key),
            "twelve_data_configured":bool(settings.twelve_data_api_key),
            "otc_enabled":False}

@router.get("/demo/account")
def demo_account(db:Session=Depends(get_db)):
    a=get_account(db); return {"balance":a.balance,"initial_balance":a.initial_balance,"currency":"USD","mode":"VIRTUAL"}

@router.post("/demo/trades")
def demo_create(payload:DemoTradeRequest,db:Session=Depends(get_db)):
    try:
        t=create_trade(db,payload.model_dump())
        return {"id":t.id,"status":t.status,"symbol":t.symbol,"direction":t.direction,"stake":t.stake}
    except Exception as e: raise HTTPException(400,str(e))

@router.post("/demo/trades/{trade_id}/settle")
def demo_settle(trade_id:int,expiry_price:float,db:Session=Depends(get_db)):
    try:
        t=settle(db,trade_id,expiry_price)
        return {"id":t.id,"status":t.status,"pnl":t.pnl,"expiry_price":t.expiry_price}
    except Exception as e: raise HTTPException(400,str(e))

@router.get("/demo/trades")
def demo_trades(db:Session=Depends(get_db)):
    rows=db.query(DemoTrade).order_by(DemoTrade.id.desc()).limit(200).all()
    return [{"id":t.id,"symbol":t.symbol,"direction":t.direction,"stake":t.stake,
        "entry_price":t.entry_price,"expiry_price":t.expiry_price,"status":t.status,"pnl":t.pnl} for t in rows]

@router.get("/signals")
def signals(limit:int=100,db:Session=Depends(get_db)):
    rows=db.query(SignalRecord).order_by(SignalRecord.id.desc()).limit(min(limit,500)).all()
    return [{"id":s.id,"created_at":s.created_at.isoformat(),"symbol":s.symbol,
        "market_type":s.market_type,"timeframe":s.timeframe,"decision":s.decision,
        "tier":s.tier,"strength_score":s.strength_score,"outcome":s.outcome,
        "explanation":s.explanation} for s in rows]

@router.get("/signals/{signal_id}")
def signal_detail(signal_id:int,db:Session=Depends(get_db)):
    s=db.query(SignalRecord).filter_by(id=signal_id).first()
    if not s: raise HTTPException(404,"Signal not found")
    return {"id":s.id,"snapshot":json.loads(s.snapshot_json)}

@router.get("/learning/summary")
def learning_summary(db:Session=Depends(get_db)):
    rows=db.query(SignalRecord).filter(SignalRecord.outcome.in_(["WIN","LOSS"])).all()
    result=summarize([x.outcome for x in rows])
    result["note"]="Only reconciled outcomes count; no automatic model promotion."
    return result

@router.get("/learning/expected-value")
def ev(win_rate:float,payout:float=.8):
    if not 0<=win_rate<=1 or not 0<=payout<=1: raise HTTPException(400,"Inputs must be between 0 and 1")
    return {"ev_per_unit_stake":expected_value(win_rate,payout),"break_even_win_rate":1/(1+payout)}
