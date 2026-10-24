"""Read-only: where the Fenix A320 places its exterior/cabin sounds, as datum-frame positions, grouped by anchor.

Each part's sound.xml anchors <Sound> elements to a NodeName (searched in that part's model, placed by its
attach node) or to the part's own origin. Prints anchor, position (lateral L/R, height, fore/aft) and events.
"""
import collections, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
import viewcheck as vc  # noqa: E402
import fnxcheck as fx  # noqa: E402
from nodes import mat_mul  # noqa: E402

preset = sys.argv[1] if len(sys.argv) > 1 else "FNX_320_CFM_SL"
WANT = ("Part_Exterior_CFM", "Part_Exterior_IAE", "Part_Exterior_Fuselage", "Part_Exterior_Wings", "Part_Exterior_Gear_Main", "Part_Interior_Cabin")
parts = {}
for kind in ("exterior", "interior"):
    for L, A, name in fx.place(fx.assemble(preset, kind)):
        parts.setdefault(name, (L, A))
for folder in WANT:
    snd = fx.resolve(os.path.join(fx.AC, "attachments", "fnx", folder, "sound", "sound.xml"))
    if not snd:
        continue
    # the part whose models live in this folder (its own attachment, or a variant attached from it)
    match = [(n, LA) for n, LA in parts.items() if n == folder or n.startswith(folder + "_") or any(("\\" + folder + "\\") in f for f in LA[0][0])]
    if not match and folder == "Part_Exterior_Fuselage":   # sound-only folder; its nodes live in the fuselage model
        match = [(n, LA) for n, LA in parts.items() if "\\Part_Exterior_Fuselage_A3" in LA[0][0][0]]
    if not match:
        print(f"== {folder}: not part of {preset}")
        continue
    name, (L, A) = match[0]
    g, nodes, world = vc.load_gltf(L[0][0])
    nm = {n.get("name", ""): i for i, n in enumerate(nodes)}
    text = re.sub(r"<!--.*?-->", "", open(snd, encoding="utf-8", errors="replace").read(), flags=re.S)
    groups = collections.defaultdict(set)
    for m in re.finditer(r"<Sound\b([^>]*)>", text):
        a = dict(re.findall(r'(\w+)="([^"]*)"', m.group(1)))
        ev = a.get("WwiseEvent") or a.get("FileName") or "?"
        anchor = a.get("NodeName") or ("ref:" + a["ReferencePointName"] if "ReferencePointName" in a else "(part origin)")
        off = tuple(float(a.get(k, 0)) for k in ("PositionX", "PositionY", "PositionZ"))
        groups[(anchor, off, a.get("ViewPoint", ""))].add(ev)
    print(f"== {folder}  (part {name}; model {os.path.basename(L[0][0])})")
    for (anchor, off, vp), evs in sorted(groups.items(), key=lambda kv: kv[0][0]):
        if anchor.startswith("ref:"):
            pos = "reference point"
        else:
            i = nm.get(anchor)
            W = world(i) if i is not None else [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
            W = mat_mul(A, W) if A else W
            x, y, z = (W[r][0] * off[0] + W[r][1] * off[1] + W[r][2] * off[2] + W[r][3] for r in range(3))
            side = "L" if x > 0.3 else "R" if x < -0.3 else "C"
            pos = f"{side} {abs(x):4.1f} m out, y {y:+.1f}, z {z:+6.2f}" + ("" if i is not None or anchor == "(part origin)" else "  (node not in model)")
        print(f"   {anchor[:34]:34s} {pos:44s} {vp[:7]:7s} {len(evs):3d}: {', '.join(sorted(evs))[:90]}")
