from statistics import mean
from math import sqrt

def ema(values, period):
    if len(values) < period: return None
    alpha = 2 / (period + 1)
    value = mean(values[:period])
    for x in values[period:]:
        value = x * alpha + value * (1-alpha)
    return value

def rsi(values, period=14):
    if len(values) <= period: return None
    diffs = [values[i]-values[i-1] for i in range(1,len(values))][-period:]
    gains = mean([max(x,0) for x in diffs])
    losses = mean([abs(min(x,0)) for x in diffs])
    return 100.0 if losses == 0 else 100 - 100/(1+gains/losses)

def atr(candles, period=14):
    if len(candles) <= period: return None
    tr=[]
    for i in range(1,len(candles)):
        c,p=candles[i],candles[i-1]
        tr.append(max(c["high"]-c["low"],abs(c["high"]-p["close"]),abs(c["low"]-p["close"])))
    return mean(tr[-period:])

def bollinger(values, period=20, deviations=2):
    if len(values)<period: return None
    sample=values[-period:]; avg=mean(sample)
    sd=sqrt(sum((x-avg)**2 for x in sample)/period)
    return {"middle":avg,"upper":avg+deviations*sd,"lower":avg-deviations*sd}
