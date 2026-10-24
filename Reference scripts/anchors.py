"""Read-only: where the iFly 737 MAX 8 and the FlyByWire A32NX anchor their sounds (sound.xml NodeName -> model node
position, datum frame). Groups events by anchor and prints lateral/height/fore-aft and the ViewPoint mix.
Usage: anchors.py ifly|fbw
"""
import collections, json, os, re, sys
S = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, S)
import viewcheck as vc  # noqa: E402

C = r"D:\MSFS2024 Community\Community"
CFG = {
    "ifly": (os.path.join(C, r"ifly-aircraft-737max8\SimObjects\Airplanes\iFly 737-MAX8\sound\sound.xml"), None),
    "fbw": (os.path.join(C, r"flybywire-aircraft-a320-neo\SimObjects\AirPlanes\FlyByWire_A320_NEO\sound\sound.xml"),
            os.path.join(C, r"flybywire-aircraft-a320-neo\SimObjects\AirPlanes\FlyByWire_A320_NEO\model\A320_NEO_LOD00.gltf")),
}
kind = sys.argv[1]
xml, model = CFG[kind]
if model is None:
    import genclassic as gc
    folder = os.path.join(gc.IFLY, "iFly 737-MAX8-189Seats", "model.189Seat")
    cfg = open(os.path.join(folder, "model.CFG"), encoding="utf-8").read()
    model = gc.model_file(os.path.normpath(os.path.join(folder, re.search(r"normal\s*=\s*(\S.*)", cfg).group(1).strip())))
text = open(xml, encoding="utf-8", errors="replace").read()
text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
g, nodes, world = vc.load_gltf(model)
pos = {}
for i, n in enumerate(nodes):
    nm = n.get("name", "")
    if nm and nm not in pos:
        W = world(i)
        pos[nm] = (W[0][3], W[1][3], W[2][3]) if isinstance(W[0], (list, tuple)) else (W[12], W[13], W[14])
groups = collections.defaultdict(list)
for m in re.finditer(r"<Sound\b([^>]*)>", text):
    a = dict(re.findall(r'(\w+)="([^"]*)"', m.group(1)))
    ev = a.get("WwiseEvent") or a.get("WwiseData") or a.get("Name") or "?"
    groups[(a.get("NodeName", "(none)"), a.get("ViewPoint", "-"))].append(ev)
print(f"{kind}: {sum(len(v) for v in groups.values())} sounds, {len(groups)} anchor/viewpoint groups; model {os.path.basename(model)}")
rows = []
for (node, vp), evs in groups.items():
    p = pos.get(node)
    rows.append((p[2] if p else -999, node, vp, evs, p))
for z, node, vp, evs, p in sorted(rows, key=lambda r: -r[0]):
    where = f"{'L' if p[0] > 0 else 'R' if p[0] < 0 else 'C'} {abs(p[0]):4.1f} m out, y {p[1]:+5.1f}, z {p[2]:+6.2f}" if p else "(node not in model)"
    print(f"   {node[:34]:34s} {where:40s} {vp:8s} {len(evs):3d}: {', '.join(sorted(set(evs)))[:150]}")
