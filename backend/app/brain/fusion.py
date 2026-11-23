from collections import defaultdict

PROFILES={"CONSERVATIVE":{"score":78,"agreement":.78},
          "BALANCED":{"score":65,"agreement":.65},
          "ACTIVE":{"score":58,"agreement":.60}}

def wait(reason,score=None,agreement=None):
    return {"decision":"WAIT","tier":"NONE",
        "strength_score":round(score,1) if score is not None else None,
        "expert_agreement":round(agreement,3) if agreement is not None else None,
        "calibrated_win_probability":None,"reason":reason}

def fuse(votes,data_quality="GOOD",profile="BALANCED"):
    if data_quality!="GOOD": return wait("Data-quality gate blocked new signal.")
    cfg=PROFILES.get(profile,PROFILES["BALANCED"])
    usable=[v for v in votes if v["data_quality"]=="GOOD" and v["direction"] in ("CALL","PUT")]
    if not usable: return wait("No valid directional expert votes.")
    weights=defaultdict(float); scores=defaultdict(float)
    for v in usable:
        d=v["direction"]; weights[d]+=v["weight"]; scores[d]+=v["strength"]*v["weight"]
    total=sum(weights.values()); direction=max(weights,key=weights.get)
    agreement=weights[direction]/total; strength=scores[direction]/weights[direction]
    if agreement<cfg["agreement"]: return wait("Experts disagree; balanced controller chose WAIT.",strength,agreement)
    if strength<cfg["score"]: return wait("Evidence below selected frequency profile.",strength,agreement)
    return {"decision":direction,"tier":"PREMIUM" if strength>=82 and agreement>=.8 else "STANDARD",
        "strength_score":round(strength,1),"expert_agreement":round(agreement,3),
        "calibrated_win_probability":None,"reason":"Experimental expert consensus; not a calibrated forecast.",
        "valid_experts":len(usable),"profile":profile}
