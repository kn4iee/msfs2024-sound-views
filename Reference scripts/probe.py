"""List mesh nodes of a glTF whose name or material matches a regex, with world-space bbox and materials.

Usage: probe.py <gltf> <regex> [max lines]
"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from nodes import local_matrix, mat_mul  # noqa: E402

path, pat = sys.argv[1], re.compile(sys.argv[2], re.I)
limit = int(sys.argv[3]) if len(sys.argv) > 3 else 60
g = json.load(open(path, encoding="utf-8"))
nodes = g["nodes"]
parent = {c: i for i, n in enumerate(nodes) for c in n.get("children", [])}


def world(i):
    m = local_matrix(nodes[i])
    while i in parent:
        i = parent[i]
        m = mat_mul(local_matrix(nodes[i]), m)
    return m


shown = 0
print(f"{os.path.basename(path)}: {len(nodes)} nodes, {len(g.get('meshes', []))} meshes, {len(g.get('materials', []))} materials")
for i, n in enumerate(nodes):
    if "mesh" not in n:
        continue
    prims = g["meshes"][n["mesh"]]["primitives"]
    mats = sorted({g["materials"][p["material"]].get("name", "?") + "[" + ",".join(k.replace("ASOBO_material_", "") for k in g["materials"][p["material"]].get("extensions", {})) + "]"
                   for p in prims if "material" in p})
    if not (pat.search(n.get("name", "")) or any(pat.search(m) for m in mats)):
        continue
    W = world(i)
    lo, hi = [1e9] * 3, [-1e9] * 3
    for p in prims:
        acc = g["accessors"][p["attributes"]["POSITION"]]
        for a in (acc["min"][0], acc["max"][0]):
            for b in (acc["min"][1], acc["max"][1]):
                for c in (acc["min"][2], acc["max"][2]):
                    v = [W[r][0] * a + W[r][1] * b + W[r][2] * c + W[r][3] for r in range(3)]
                    lo = [min(lo[k], v[k]) for k in range(3)]
                    hi = [max(hi[k], v[k]) for k in range(3)]
    print(f"  {n.get('name', '?')[:40]:40s} x {lo[0]:+6.2f}..{hi[0]:+6.2f} y {lo[1]:+5.2f}..{hi[1]:+5.2f} z {lo[2]:+6.2f}..{hi[2]:+6.2f}  {', '.join(mats)[:110]}")
    shown += 1
    if shown >= limit:
        print("  ...")
        break
