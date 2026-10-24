"""Run viewcheck on one preset.

Usage: checkrun.py <preset dir> <eye lon ft> <eye lat ft> <eye vert ft> <cameras.CFG> <out dir> [extra.json] [--slots 1,2] [--hfov 70]
extra.json: {"name": [[x,y,z],[pitch,bank,heading],zoom], ...}  (camera-file style values)
"""
import json, math, os, re, sys, time
sys.path.insert(0, os.path.dirname(__file__))
import viewcheck as vc  # noqa: E402

args, opts, _i = [], {}, 1
while _i < len(sys.argv):
    if sys.argv[_i].startswith("--"):
        opts[sys.argv[_i][2:]] = sys.argv[_i + 1]
        _i += 2
    else:
        args.append(sys.argv[_i])
        _i += 1
preset, lon_ft, lat_ft, vert_ft, camfile, outdir = args[:6]
extra = json.load(open(args[6])) if len(args) > 6 else {}
if "hfov" in opts:
    vc.HFOV_044 = float(opts["hfov"])
eye = (float(lon_ft) * vc.FT, float(lat_ft) * vc.FT, float(vert_ft) * vc.FT)
os.makedirs(outdir, exist_ok=True)
pkg = preset[:preset.lower().index("\\simobjects\\")]

cams = vc.read_cameras(camfile, eye) if os.path.exists(camfile) else {}
if "slots" in opts:
    cams = {k: v for k, v in cams.items() if k in opts["slots"].split(",")}
for name, (xyz, pbh, zoom) in extra.items():
    cams[name] = vc.camera(tuple(xyz), (math.radians(pbh[0]), math.radians(pbh[2])), eye, zoom)

t0 = time.time()
spheres = [(c[0][0], c[0][1], c[0][2], vc.R_INT) for c in cams.values()]
parts, merged = vc.assemble(pkg, os.path.join(preset, "config"), "interior", 0)
mats = vc.node_mats(merged)
tris = []
for path, node, xml, off in parts:
    attach = vc.attach_matrix(mats, node, off)
    if node and attach is None:
        print("  ! attach node not found:", node, "for", xml)
    cls = 6 if re.search(r"cockpit|_VC", xml + path, re.I) else 5 if re.search(r"seat|ECOS|FCS|sofa|BR_|table", xml, re.I) else 4
    if cls in (5, 6) and re.search(r"LOD0", path) and os.path.exists(path.replace("LOD0", "LOD1")):
        path = path.replace("LOD0", "LOD1")
    n = vc.load_tris(path, attach, cls, spheres, tris)
    if n:
        print(f"  interior {os.path.basename(path):34s} node={node or '-':16s} +{n} tris")
ext_parts, ext_merged = vc.assemble(pkg, os.path.join(preset, "config"), "exterior", 3)
etris = []
big = [(s[0], s[1], s[2], 80.0) for s in spheres[:1]]
for path, node, xml, off in ext_parts:
    cls = 3 if re.search(r"engine|eng[lr]_", path, re.I) else 2
    n = vc.load_tris(path, None, cls, big, etris)
    if n:
        print(f"  exterior {os.path.basename(path):34s} +{n} tris")
ground_y = min((t[5][1] for t in etris), default=-5.0)
print(f"loaded {len(tris)} interior / {len(etris)} exterior triangles in {time.time() - t0:.1f}s; ground y {ground_y:.2f}")
gin = vc.Grid(tris, 0.12) if tris else None
gext = vc.Grid(etris, 1.0) if etris else None
print(f"grids built {time.time() - t0:.1f}s")

report = {}
for name, cam in sorted(cams.items()):
    t1 = time.time()
    enc = vc.enclosure(cam, gin)
    img, counts, core = vc.render(cam, gin, gext, ground_y)
    vc.write_png(os.path.join(outdir, f"view_{name}.png"), img)
    tot, ctot = sum(counts), sum(core)
    pct = lambda arr, ks, T: round(100 * sum(arr[k] for k in ks) / T)
    center = vc.NAMES[img[len(img) // 2][len(img[0]) // 2]]
    rep = {"outside_core%": pct(core, (0, 1, 2, 3), ctot), "wing_engine_core%": pct(core, (2, 3), ctot),
           "interior_core%": pct(core, (4, 5, 6), ctot), "bad_all%": pct(counts, (7, 8), tot),
           "enclosure%": round(100 * enc), "center": center}
    report[name] = rep
    print(f"view {name:>10}: {rep}  ({time.time() - t1:.1f}s)")
json.dump(report, open(os.path.join(outdir, "report.json"), "w"), indent=1)
