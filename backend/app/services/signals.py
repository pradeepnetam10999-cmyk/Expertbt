import json
from app.models.tables import SignalRecord
from app.brain.experts import analyze
from app.brain.fusion import fuse

def evaluate(db,payload):
    if payload["market_type"]=="OTC":
        return {"decision":"WAIT","tier":"NONE","strength_score":None,"expert_agreement":None,
            "calibrated_win_probability":None,
            "reason":"OTC feed not configured. Broker-specific OTC data is required."}
    candles=[c.model_dump() if hasattr(c,"model_dump") else c for c in payload.get("candles",[])]
    votes=analyze(candles,payload["market_type"],payload["expiry_seconds"],
                  data_quality=payload["data_quality"])
    result=fuse(votes,payload["data_quality"],payload["profile"]); result["experts"]=votes
    rec=SignalRecord(symbol=payload["symbol"],market_type=payload["market_type"],
        timeframe=payload["timeframe"],expiry_seconds=payload["expiry_seconds"],
        decision=result["decision"],tier=result.get("tier","NONE"),
        strength_score=result.get("strength_score") or 0,
        agreement=result.get("expert_agreement") or 0,
        explanation=result.get("reason",""),snapshot_json=json.dumps(result))
    db.add(rec); db.commit(); db.refresh(rec); result["signal_id"]=rec.id
    return result
