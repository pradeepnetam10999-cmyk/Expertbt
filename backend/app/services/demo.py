from app.models.tables import DemoAccount,DemoTrade

def get_account(db):
    acc=db.query(DemoAccount).first()
    if not acc:
        acc=DemoAccount(balance=10000,initial_balance=10000); db.add(acc); db.commit(); db.refresh(acc)
    return acc

def create_trade(db,data):
    acc=get_account(db)
    if data["stake"]>acc.balance: raise ValueError("Insufficient virtual balance")
    acc.balance-=data["stake"]; trade=DemoTrade(**data); db.add(trade); db.commit(); db.refresh(trade)
    return trade

def settle(db,trade_id,expiry_price):
    t=db.query(DemoTrade).filter_by(id=trade_id).first()
    if not t: raise ValueError("Trade not found")
    if t.status!="OPEN": raise ValueError("Trade is already settled")
    acc=get_account(db); t.expiry_price=expiry_price
    won=expiry_price>t.entry_price if t.direction=="CALL" else expiry_price<t.entry_price
    if expiry_price==t.entry_price:
        t.status="TIE"; t.pnl=0; acc.balance+=t.stake
    elif won:
        t.status="WON"; t.pnl=t.stake*t.payout_rate; acc.balance+=t.stake+t.pnl
    else:
        t.status="LOST"; t.pnl=-t.stake
    db.commit(); db.refresh(t); return t
