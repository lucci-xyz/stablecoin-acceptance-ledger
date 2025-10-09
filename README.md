# Stablecoin Acceptance Ledger

A tiny, public registry of merchants and their stablecoin payment capabilities, plus a minimal API and router.

## Structure

```
stablecoin-acceptance-ledger/
merchants/               # one JSON per merchant (domain-based filename)
schemas/                 # JSON Schema(s) for validation (optional)
scripts/                 # build/validate/route helpers
dist/                    # built snapshot (index.json + hash)
api/                     # FastAPI app (main.py)
```

## Quick start

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# optional: validate merchant files if you use schemas
python scripts/validate.py

# build index snapshot
python scripts/build_index.py

# run API (dev hot-reload)
python -m fastapi dev api/main.py

# or production-ish
python -m fastapi run api/main.py
```

## API

- `GET /health` → `{"ok": true}`
- `GET /merchants?domain=walmart.com` → merchant capability object
  - Without domain returns `{"count": N}`.
- `GET /route?domain=walmart.com&asset=USDC&chain=Base` → chosen route:
  - `{"route":"stablecoin","via":"CoinbaseCommerce","asset":"USDC","chain":"Base"}`
  - `{"route":"fiat_convert","via":"ACH"}`
  - `{"route":"proxy","via":"GiftCardAPI"}`

## Merchant file schema (example)

`merchants/walmart.com.json`

```json
{
  "merchant_id": "walmart.com",
  "display_name": "Walmart",
  "accepts": [
    {"asset":"USDC","chain":"Base","via":"CoinbaseCommerce","confidence":0.9}
  ],
  "fiat_routes": ["ACH","Card"],
  "proxies": ["GiftCardAPI","BillPayX"],
  "payment_pages": ["https://www.walmart.com/checkout"],
  "last_verified": "2025-10-09T18:00:00Z",
  "verified_by": ["user:0xABCD..."],
  "evidence": ["url:https://.../payments","tx:base:0x..."]
}
```

Keep entries human-readable, include at least one evidence item, and update last_verified when you change capabilities.

## Build snapshot

`python scripts/build_index.py` aggregates `merchants/*.json` into `dist/index.json` and writes `dist/index.sha256` for tamper hints.

## Contributing

1. Add or update `merchants/<domain>.json` following the example.
2. Include evidence.
3. Run `python scripts/build_index.py` locally to ensure it builds.
4. Open a PR.

## License

MIT. See LICENSE.