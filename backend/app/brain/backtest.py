from app.brain.experts import analyze
from app.brain.fusion import fuse

def run_backtest(candles,expiry_bars=1,profile="BALANCED",market_type="NON_OTC"):
    trades=[]
    for i in range(30,len(candles)-expiry_bars):
        hist=candles[:i+1]
        result=fuse(analyze(hist,market_type,expiry_bars*60),profile=profile)
        if result["decision"]=="WAIT": continue
        entry=hist[-1]["close"]; exit_price=candles[i+expiry_bars]["close"]
        won=exit_price>entry if result["decision"]=="CALL" else exit_price<entry
        trades.append({"index":i,"direction":result["decision"],"entry":entry,
                       "exit":exit_price,"outcome":"WIN" if won else "LOSS"})
    wins=sum(t["outcome"]=="WIN" for t in trades); n=len(trades)
    return {"trades":n,"wins":wins,"losses":n-wins,"win_rate":wins/n if n else None,
            "results":trades,"warning":"Simplified candle-close research test; excludes payout, spread, latency and execution effects."}
