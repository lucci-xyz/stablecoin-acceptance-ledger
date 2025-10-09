import json, pathlib, hashlib, sys
root = pathlib.Path(__file__).resolve().parents[1]
merchants = []
for p in sorted((root/"merchants").glob("*.json")):
    data = json.loads(p.read_text())
    merchants.append(data)
index = {"version":"v1", "count":len(merchants), "merchants":merchants}
out = root/"dist"/"index.json"
out.parent.mkdir(exist_ok=True)
out.write_text(json.dumps(index, separators=(",",":")))
# write a hash for tamper hints
h = hashlib.sha256(out.read_bytes()).hexdigest()
(root/"dist"/"index.sha256").write_text(h+"\n")
print(f"wrote {out} ({len(merchants)}), sha256={h[:12]}")