"""List a glTF's materials (name, alpha, extensions) with how many mesh primitives use each. Usage: mats.py <gltf> [regex]"""
import collections, json, re, sys

g = json.load(open(sys.argv[1], encoding="utf-8"))
pat = re.compile(sys.argv[2], re.I) if len(sys.argv) > 2 else None
use = collections.Counter(p.get("material") for m in g.get("meshes", []) for p in m["primitives"])
for i, m in enumerate(g.get("materials", [])):
    label = f"{m.get('name', '?')} [{m.get('alphaMode', 'OPAQUE')}] " + ",".join(k.replace("ASOBO_material_", "") for k in m.get("extensions", {}))
    if pat is None or pat.search(label):
        print(f"{use[i]:5d}  {label}")
