from __future__ import annotations
import json, subprocess, pathlib
from fastapi import FastAPI, HTTPException, Query

ROOT = pathlib.Path(__file__).resolve().parents[1]
DIST = ROOT / "dist" / "index.json"
BUILD = ROOT / "scripts" / "build_index.py"

app = FastAPI(title="Stablecoin Acceptance Ledger", version="1.0")

def build_index() -> None:
    DIST.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["python", str(BUILD)], cwd=str(ROOT), check=True)

def load_index() -> dict:
    if not DIST.exists():
        build_index()
    return json.loads(DIST.read_text())

INDEX = load_index()

def get_merchant(domain: str) -> dict | None:
    for m in INDEX.get("merchants", []):
        if m.get("merchant_id") == domain:
            return m
    return None

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/merchants")
def merchants(domain: str | None = Query(default=None, description="e.g. walmart.com")):
    if not domain:
        return {"count": INDEX.get("count", 0)}
    m = get_merchant(domain)
    if not m:
        raise HTTPException(404, "merchant not found")
    return m

@app.get("/route")
def route(domain: str, asset: str = "USDC", chain: str = "Base"):
    m = get_merchant(domain)
    if not m:
        raise HTTPException(404, "merchant not found")

    # 1) direct stablecoin match
    for a in m.get("accepts", []):
        if a.get("asset") == asset and a.get("chain") == chain:
            return {"route": "stablecoin", "via": a.get("via"), "asset": asset, "chain": chain}

    # 2) fiat rails
    if m.get("fiat_routes"):
        return {"route": "fiat_convert", "via": m["fiat_routes"][0]}

    # 3) proxy rails
    if m.get("proxies"):
        return {"route": "proxy", "via": m["proxies"][0]}

    raise HTTPException(400, "no supported route")