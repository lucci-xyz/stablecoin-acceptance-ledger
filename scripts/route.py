import json, sys
# usage: python scripts/route.py domain asset=USDC chain=Base
domain = sys.argv[1]
kv = dict(x.split("=",1) for x in sys.argv[2:])
asset = kv.get("asset","USDC"); chain = kv.get("chain","Base")

index = json.load(open("dist/index.json"))
m = next((m for m in index["merchants"] if m["merchant_id"]==domain), None)

def pick_route(m):
    if m:
        # 1) direct stablecoin if exact match exists
        for a in m.get("accepts", []):
            if a["asset"]==asset and a["chain"]==chain:
                return {"route":"stablecoin", "via":a["via"], "why":"direct acceptance"}
        # 2) fiat if available
        if m.get("fiat_routes"): return {"route":"fiat_convert", "via":m["fiat_routes"][0], "why":"fiat rails"}
        # 3) proxy gift/bill-pay
        if m.get("proxies"): return {"route":"proxy", "via":m["proxies"][0], "why":"proxy rails"}
    # 4) unsupported
    return {"route":"fail","why":"no capability known"}

print(json.dumps(pick_route(m)))