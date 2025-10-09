import json, pathlib, sys
from jsonschema import validate, Draft202012Validator

root = pathlib.Path(__file__).resolve().parents[1]
schema = json.loads((root/"schemas"/"merchant.schema.json").read_text())
errors = 0
for p in sorted((root/"merchants").glob("*.json")):
    data = json.loads(p.read_text())
    v = Draft202012Validator(schema)
    errs = sorted(v.iter_errors(data), key=lambda e: e.path)
    if errs:
        errors += 1
        print(f"[FAIL] {p.name}")
        for e in errs: print("  -", e.message)
    else:
        print(f"[OK]   {p.name}")
if errors: sys.exit(1)