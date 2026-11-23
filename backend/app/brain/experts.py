from app.brain.indicators import ema,rsi,atr

EXPERTS=["market_structure","candlestick","price_action","indicators","expiry_intelligence",
"entry_timing","volatility","multi_timeframe","market_psychology","sessions","otc_intelligence",
"news_intelligence","probability","strategy","confirmation","risk_intelligence",
"data_intelligence","learning_engine","signal_intelligence","self_monitoring"]

def vote(module,direction="NEUTRAL",strength=0,reason="No validated evidence",weight=1,quality="GOOD"):
    return {"module":module,"direction":direction,"strength":float(strength),
            "weight":float(weight),"data_quality":quality,"reason":reason}

def analyze(candles,market_type="NON_OTC",expiry_seconds=60,session="UNKNOWN",news_risk=False,data_quality="GOOD"):
    if market_type=="OTC":
        return [vote(x,reason="OTC feed not configured; standard market data is not an OTC proxy",
                     quality="DEGRADED" if x=="otc_intelligence" else "GOOD") for x in EXPERTS]
    if data_quality!="GOOD" or len(candles)<25:
        return [vote(x,reason="Insufficient history or data-quality gate") for x in EXPERTS]
    closes=[c["close"] for c in candles]; c=candles[-1]
    body=c["close"]-c["open"]; rng=max(c["high"]-c["low"],1e-12)
    ratio=abs(body)/rng; upper=c["high"]-max(c["open"],c["close"])
    lower=min(c["open"],c["close"])-c["low"]
    fast,slow=ema(closes,9),ema(closes,21); momentum=rsi(closes); vol=atr(candles)
    out=[]
    up=sum(closes[i]>closes[i-1] for i in range(len(closes)-5,len(closes)))
    dn=5-up
    out.append(vote("market_structure","CALL" if up>=4 else "PUT" if dn>=4 else "NEUTRAL",70 if max(up,dn)>=4 else 0,"Recent swing-direction proxy"))
    if ratio>.55 and body!=0: out.append(vote("candlestick","CALL" if body>0 else "PUT",76,"Strong candle body"))
    elif lower>upper*1.8 and lower>rng*.35: out.append(vote("candlestick","CALL",68,"Lower wick rejection candidate"))
    elif upper>lower*1.8 and upper>rng*.35: out.append(vote("candlestick","PUT",68,"Upper wick rejection candidate"))
    else: out.append(vote("candlestick",reason="No strong candle pattern"))
    hi=max(x["high"] for x in candles[-21:-1]); lo=min(x["low"] for x in candles[-21:-1])
    if c["close"]>hi: out.append(vote("price_action","CALL",78,"Close above recent range"))
    elif c["close"]<lo: out.append(vote("price_action","PUT",78,"Close below recent range"))
    else: out.append(vote("price_action",reason="No range break"))
    if fast and slow and momentum is not None and fast>slow and momentum<72: out.append(vote("indicators","CALL",72,f"EMA alignment; RSI {momentum:.1f}"))
    elif fast and slow and momentum is not None and fast<slow and momentum>28: out.append(vote("indicators","PUT",72,f"EMA alignment; RSI {momentum:.1f}"))
    else: out.append(vote("indicators",reason="Indicators not aligned"))
    out.append(vote("expiry_intelligence",reason=f"{expiry_seconds}s expiry needs separate expiry-specific validation"))
    out.append(vote("entry_timing","CALL" if body>0 else "PUT" if body<0 else "NEUTRAL",65 if ratio>.65 else 0,"Strong candle close candidate" if ratio>.65 else "Wait for confirmation"))
    out.append(vote("volatility",reason="Extreme candle guard" if vol and rng>vol*1.7 else "No volatility expansion signal"))
    out.append(vote("multi_timeframe",reason="Higher timeframe context not supplied"))
    out.append(vote("market_psychology","CALL" if body>0 else "PUT" if body<0 else "NEUTRAL",60 if ratio>.7 else 0,"Candle pressure proxy, not direct sentiment"))
    out.append(vote("sessions",reason=f"Session {session}; not yet statistically calibrated"))
    out.append(vote("otc_intelligence",reason="Not applicable to non-OTC market"))
    out.append(vote("news_intelligence",quality="DEGRADED" if news_risk else "GOOD",reason="News risk flag active" if news_risk else "Calendar adapter not configured"))
    out.append(vote("probability",reason="No calibrated historical probability model"))
    if fast and slow and fast>slow: out.append(vote("strategy","CALL",64,"Trend-following candidate"))
    elif fast and slow and fast<slow: out.append(vote("strategy","PUT",64,"Trend-following candidate"))
    else: out.append(vote("strategy",reason="No trend candidate"))
    out.append(vote("confirmation",reason="Caller must provide closed-candle confirmation"))
    out.append(vote("risk_intelligence",reason="Risk guard is applied at virtual trade placement"))
    out.append(vote("data_intelligence",reason="Basic data gate passed; provider lineage still required"))
    out.append(vote("learning_engine",reason="Learning requires validated outcome dataset"))
    out.append(vote("signal_intelligence",reason="Fusion engine owns final decision"))
    out.append(vote("self_monitoring",reason="Runtime health monitor owns service status"))
    return out
