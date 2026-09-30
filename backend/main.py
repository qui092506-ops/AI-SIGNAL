from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from datetime import datetime, timezone
import os, random

BASE=Path(__file__).resolve().parent
app=FastAPI(title="AI SIGNAL — XAUUSD Signal API")

# DEMO provider by default. Replace get_market_snapshot() with a licensed/live
# XAUUSD market-data provider before publishing as a real-time signal service.
LIVE=os.getenv("LIVE_MODE","false").lower()=="true"

def get_market_snapshot():
    # Safe demo data so the website works immediately without pretending it is live.
    base=2650.0 + random.uniform(-8,8)
    return {"price": round(base,2), "change": "+0.00%", "live": False}

def generate_signal(m):
    # Placeholder deterministic interface for the strategy layer.
    # Production version should feed M1/M5/M15 OHLC data into a validated
    # strategy with ATR, structure, liquidity, spread and news filters.
    return {
        "signal":"WAIT","score":0,
        "m15":"NEUTRAL","m5":"WAIT","m1":"WAIT",
        "entry":"—","sl":"—","tp1":"—","tp2":"—","tp3":"—","rr":"—",
        "news":"UNKNOWN","last":"—",
        "reasons":["No live OHLC feed is connected.","Demo mode intentionally does not fabricate a BUY/SELL setup."]
    }

@app.get("/api/signal")
def signal(symbol:str="XAUUSD"):
    m=get_market_snapshot()
    s=generate_signal(m)
    return {**m, **s, "timestamp":datetime.now(timezone.utc).isoformat()}

app.mount("/static", StaticFiles(directory=BASE.parent/"frontend"), name="static")
@app.get("/")
def home():
    return FileResponse(BASE.parent/"frontend"/"index.html")
