def summarize(labels):
    wins=sum(x=="WIN" for x in labels); losses=sum(x=="LOSS" for x in labels); n=wins+losses
    return {"wins":wins,"losses":losses,"sample_size":n,
            "win_rate":round(wins/n,4) if n else None,
            "status":"INSUFFICIENT_SAMPLE" if n<100 else "DESCRIPTIVE_ONLY"}

def expected_value(win_rate,payout):
    return None if win_rate is None else win_rate*payout-(1-win_rate)

def promotion_gate(champion,challenger,min_samples=200):
    if challenger.get("sample_size",0)<min_samples:
        return {"recommendation":"MORE_DATA","reason":"Insufficient out-of-sample sample size"}
    a,b=champion.get("expected_value"),challenger.get("expected_value")
    if a is None or b is None: return {"recommendation":"MANUAL_REVIEW","reason":"Missing comparable metrics"}
    return {"recommendation":"REVIEW_CANDIDATE" if b>a else "KEEP_CHAMPION",
            "reason":"Offline comparison only; no automatic model promotion"}
