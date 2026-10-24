"""Search nearby camera positions for views that fail the offline check, and rewrite the camera file.

Usage: autofix.py <label> [--write] [--slots 4,8]
<label> selects one RUNS entry from batch.py (substring match). Without --slots, fixes every cabin slot that fails.
"""
import math, os, re, sys, time
sys.path.insert(0, os.path.dirname(__file__))
import viewcheck as vc  # noqa: E402
from batch import RUNS, C, R  # noqa: E402
from gen737 import mesh_points, window_centers  # noqa: E402

FT = vc.FT


def opt(name, default=None):
    return sys.argv[sys.argv.index("--" + name) + 1] if "--" + name in sys.argv else default


label = sys.argv[1]
run = next(r for r in RUNS if label in r[0])
lab, pkg, ac, preset, lon_ft, lat_ft, vert_ft = run
eye = (lon_ft * FT, lat_ft * FT, vert_ft * FT)
pdir = os.path.join(C, pkg, "SimObjects", "Airplanes", ac, "presets", "pmdg", preset)
camfile = os.path.join(R, ac, "presets", "pmdg", preset, "config", "cameras.CFG")
pkgroot = os.path.join(C, pkg)

# ---- camera file
text = open(camfile, encoding="utf-8").read()
blocks = re.split(r"(?=\[CAMERADEFINITION\.\d+\])", text)
cams = {}
for b in blocks:
    t = re.search(r'Title="([^"]*)"', b)
    if not t:
        continue
    xyz = [float(v) for v in re.search(r"InitialXyz=\s*([^\r\n]+)", b).group(1).split(",")]
    pbh = [float(v) for v in re.search(r"InitialPbh=\s*([^\r\n]+)", b).group(1).split(",")]
    zoom = float(re.search(r"InitialZoom=\s*([-\d.]+)", b).group(1))
    cams[t.group(1)] = (xyz, pbh, zoom)

# ---- geometry (interior near all cabin cameras + exterior)
def to_cam(xyz, pbh, zoom):
    return vc.camera(tuple(xyz), (math.radians(pbh[0]), math.radians(pbh[2])), eye, zoom)


cabin_slots = [s for s in "12345678" if s in cams]
spheres = [(*to_cam(*cams[s])[0], 4.5) for s in cabin_slots]
parts, merged = vc.assemble(pkgroot, os.path.join(pdir, "config"), "interior", 0)
mats = vc.node_mats(merged)
tris = []
for path, node, xml, off in parts:
    cls = 6 if re.search(r"cockpit|_VC", xml + path, re.I) else 5 if re.search(r"seat|ECOS|FCS|sofa|BR_|table", xml, re.I) else 4
    if cls in (5, 6) and "LOD0" in path and os.path.exists(path.replace("LOD0", "LOD1")):
        path = path.replace("LOD0", "LOD1")
    vc.load_tris(path, vc.attach_matrix(mats, node, off), cls, spheres, tris)
eparts, _ = vc.assemble(pkgroot, os.path.join(pdir, "config"), "exterior", 3)
etris = []
for path, node, xml, off in eparts:
    vc.load_tris(path, None, 3 if re.search(r"engine|eng[lr]_", path, re.I) else 2, [(*spheres[0][:3], 80.0)], etris)
ground_y = min((t[5][1] for t in etris), default=-5.0)
gin, gext = vc.Grid(tris, 0.12), vc.Grid(etris, 1.0)

# windows of the fuselage actually used (exterior LOD0 glass meshes)
win_pts = []
for path, node, xml, off in vc.assemble(pkgroot, os.path.join(pdir, "config"), "exterior", 0)[0]:
    win_pts += mesh_points(path, r"^(cabin_windows|cabin_window_glass\d*|pax_window_glass|900ER_pax_window_glass)$")
wins = {s: window_centers(win_pts, s) for s in "LR"}
glass_lat = (sum(abs(p[0]) for p in win_pts) / len(win_pts)) if win_pts else None


def evaluate(xyz, pbh, zoom, w=32, h=18):
    cam = to_cam(xyz, pbh, zoom)
    img, counts, core = vc.render(cam, gin, gext, ground_y, w, h)
    tot, ctot = sum(counts), sum(core)
    bad = 100 * (counts[7] + counts[8]) / tot
    out = 100 * sum(core[k] for k in (0, 1, 2, 3)) / ctot
    wing = 100 * (core[2] + core[3]) / ctot
    center = img[h // 2][w // 2]
    return bad, out, wing, center, img


def score(bad, out, wing, center, dist, dh):
    if bad > 5 or center in (7, 8):
        return -1000 - bad
    return out + 0.5 * wing - 3 * bad - 12 * dist - 0.3 * abs(dh)


def rel_from_abs(lat_r, y_abs, lon):
    return [lat_r - eye[1], y_abs - eye[2], lon - eye[0]]


slots = opt("slots", "").split(",") if opt("slots") else None
changed = {}
for s in cabin_slots:
    xyz, pbh, zoom = cams[s]
    bad0, out0, wing0, c0, _ = evaluate(xyz, pbh, zoom, 96, 54)
    lat_r, y_abs, lon = xyz[0] + eye[1], xyz[1] + eye[2], xyz[2] + eye[0]
    side = "L" if lat_r < 0 else "R"
    sign = -1 if side == "L" else 1
    has_win = len(wins[side]) >= 6
    fails = bad0 > 5 or c0 in (7, 8) or (has_win and out0 < 15)
    if slots is not None and s not in slots:
        continue
    if slots is None and not fails:
        print(f"slot {s}: ok (outside {out0:.0f}%, bad {bad0:.0f}%, center {vc.NAMES[c0]})")
        continue
    t0 = time.time()
    cands = []
    if has_win:
        near = sorted(wins[side], key=lambda wz: abs(wz - lon))[:5]
        insets = [0.20, 0.30, 0.40, 0.50, 0.60] if glass_lat > 2.5 else [0.15, 0.22, 0.30, 0.38, 0.46]
        for wz in near:
            for ins in insets:
                cands.append((sign * (glass_lat - ins), y_abs, wz, 0.0))
    else:
        for dz in (0.0, 0.3, -0.3, 0.6, -0.6, 1.0, -1.0):
            for dl in (0.0, -0.15, -0.3, -0.45, -0.7):
                for dy in (0.0, 0.25, 0.45, -0.3):
                    cands.append((sign * (abs(lat_r) + dl), y_abs + dy, lon + dz, 0.0))
    scored = []
    for (lr, ya, lz, dh) in cands:
        x = rel_from_abs(lr, ya, lz)
        b, o, wg, c, _ = evaluate(x, pbh, zoom)
        scored.append((score(b, o, wg, c, abs(lz - lon), 0), lr, ya, lz))
    scored.sort(reverse=True)
    best = None
    for sc, lr, ya, lz in scored[:2]:
        for dh in (0, 10, -10):
            for dz in (0.0, 0.08):
                for dy in (0.0,):
                    x = rel_from_abs(lr, ya + dy, lz + dz)
                    p2 = [pbh[0], pbh[1], pbh[2] + dh]
                    b, o, wg, c, _ = evaluate(x, p2, zoom)
                    sc2 = score(b, o, wg, c, abs(lz + dz - lon), dh)
                    if best is None or sc2 > best[0]:
                        best = (sc2, x, p2, b, o, wg, c)
    sc, x, p2, b, o, wg, c = best
    bF, oF, wgF, cF, img = evaluate(x, p2, zoom, 96, 54)
    print(f"slot {s}: was outside {out0:.0f}% bad {bad0:.0f}% center {vc.NAMES[c0]}  ->  lon {x[2] + eye[0]:.2f} (moved {x[2] + eye[0] - lon:+.2f} m), "
          f"lat {x[0] + eye[1]:+.2f}, hdg {p2[2]:+.0f}: outside {oF:.0f}% bad {bF:.0f}% center {vc.NAMES[cF]}  ({time.time() - t0:.0f}s)")
    if sc > -1000 and (fails or slots is not None):
        changed[s] = (x, p2)
        out_dir = os.path.join(os.path.dirname(__file__), "vc", preset.replace(" ", "_"))
        os.makedirs(out_dir, exist_ok=True)
        vc.write_png(os.path.join(out_dir, f"fixed_{s}.png"), img)

if changed and "--write" in sys.argv:
    out = []
    for b in blocks:
        t = re.search(r'Title="([^"]*)"', b)
        if t and t.group(1) in changed:
            x, p2 = changed[t.group(1)]
            b = re.sub(r"InitialXyz=\s*[^\r\n]+", "InitialXyz= {:.6f}, {:.6f}, {:.6f}".format(*x), b)
            b = re.sub(r"InitialPbh=\s*[^\r\n]+", "InitialPbh= {:.6f}, {:.6f}, {:.6f}".format(*p2), b)
        out.append(b)
    open(camfile, "w", encoding="utf-8", newline="\r\n").write("".join(out).replace("\r\n", "\n"))
    print("written:", camfile)
