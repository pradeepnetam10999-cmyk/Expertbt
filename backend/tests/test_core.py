from app.brain.fusion import fuse
from app.brain.quality import TickGuard
from app.brain.candles import CandleBuilder
from app.brain.learning import expected_value,summarize

def v(d,s=85): return {"module":"x","direction":d,"strength":s,"weight":1,"data_quality":"GOOD","reason":"test"}

def test_conflict_waits():
    assert fuse([v("CALL"),v("PUT")])["decision"]=="WAIT"

def test_consensus():
    x=fuse([v("CALL",88),v("CALL",84)])
    assert x["decision"]=="CALL" and x["tier"]=="PREMIUM"
    assert x["calibrated_win_probability"] is None

def test_invalid_feed_waits():
    assert fuse([v("CALL")],data_quality="INVALID")["decision"]=="WAIT"

def test_tick_duplicate():
    g=TickGuard(); t={"price":1.2,"timestamp":1000}
    assert g.check("EURUSD",t,1000)[0]
    assert not g.check("EURUSD",t,1000)[0]

def test_candle_builder():
    b=CandleBuilder(60); b.ingest("X",121,1.0); b.ingest("X",125,1.2)
    assert b.snapshot("X")["high"]==1.2

def test_binary_ev():
    assert round(1/(1+.8),4)==.5556
    assert round(expected_value(.6,.8),2)==.08

def test_learning_sample_guard():
    assert summarize(["WIN","LOSS"])["status"]=="INSUFFICIENT_SAMPLE"
