"""Overall world bbox of a glTF's meshes, optionally only nodes/materials matching a regex. Usage: bbox.py <gltf> [regex]"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from nodes import local_matrix, mat_mul  # noqa: E402

g = json.load(open(sys.argv[1], encoding="utf-8"))
pat = re.compile(sys.argv[2], re.I) if len(sys.argv) > 2 else None
nodes = g["nodes"]
parent = {c: i for i, n in enumerate(nodes) for c in n.get("children", [])}


def world(i):
    m = local_matrix(nodes[i])
    while i in parent:
        i = parent[i]
        m = mat_mul(local_matrix(nodes[i]), m)
    return m


lo, hi, count = [1e9] * 3, [-1e9] * 3, 0
for i, n in enumerate(nodes):
    if "mesh" not in n:
        continue
    prims = g["meshes"][n["mesh"]]["primitives"]
    mats = [g["materials"][p["material"]].get("name", "") for p in prims if "material" in p]
    if pat and not (pat.search(n.get("name", "")) or any(pat.search(m) for m in mats)):
        continue
    W = world(i)
    for p in prims:
        acc = g["accessors"][p["attributes"]["POSITION"]]
        for a in (acc["min"][0], acc["max"][0]):
            for b in (acc["min"][1], acc["max"][1]):
                for c in (acc["min"][2], acc["max"][2]):
                    v = [W[r][0] * a + W[r][1] * b + W[r][2] * c + W[r][3] for r in range(3)]
                    lo = [min(lo[k], v[k]) for k in range(3)]
                    hi = [max(hi[k], v[k]) for k in range(3)]
    count += 1
print(f"{os.path.basename(sys.argv[1])} [{sys.argv[2] if pat else 'all'}]: {count} mesh nodes; x {lo[0]:+.2f}..{hi[0]:+.2f}  y {lo[1]:+.2f}..{hi[1]:+.2f}  z {lo[2]:+.2f}..{hi[2]:+.2f}")
