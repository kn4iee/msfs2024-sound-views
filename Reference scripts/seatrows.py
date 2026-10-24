"""Read-only: which passenger seat each cabin view (Alt+1-8) sits at, for every view file in the set.

For each cabin layout, load only the seat models, take the window-seat backs on each side (inboard of the
camera, upper seat-back height), group them into rows front to back, and give each camera the row whose seat
back is just behind it. Letters: A/F on narrowbodies; on the 777 the right window letter follows the number
of seats abreast. Writes seats.json (keyed by view file, relative to the SimObjects\\Airplanes folder).
"""
import glob, json, math, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
import viewcheck as vc  # noqa: E402

ROAM = os.path.expandvars(r"%APPDATA%\Microsoft Flight Simulator 2024\SimObjects\Airplanes")
C = r"D:\MSFS2024 Community\Community"
OUT = os.path.join(os.path.dirname(__file__), "seats.json")
FT = 0.3048


def verts(tris):
    for t in tris:
        a = t[0]
        yield a
        yield (a[0] + t[1][0], a[1] + t[1][1], a[2] + t[1][2])
        yield (a[0] + t[2][0], a[1] + t[2][1], a[2] + t[2][2])


def rows_for_side(tris, sign, lat_cam, y_cam):
    """Seat-back clusters on one side, front first: [(zmin, zmax)]. sign +1 = left (glTF +x), -1 = right."""
    zs = sorted(v[2] for v in verts(tris) if lat_cam - 0.8 <= sign * v[0] <= lat_cam + 0.1 and y_cam - 0.5 <= v[1] <= y_cam + 0.05)
    clusters, cur = [], []
    for z in zs:
        if cur and z - cur[-1] > 0.15:
            clusters.append(cur)
            cur = []
        cur.append(z)
    if cur:
        clusters.append(cur)
    clusters = [c for c in clusters if len(c) >= 12]          # ignore stray bits
    return sorted(((min(c), max(c)) for c in clusters), key=lambda r: -r[1])


def abreast(tris, y_band, z_band):
    """Seat blocks across one row: widths between aisles -> seats per block (0.46 m per seat)."""
    xs = sorted(v[0] for v in verts(tris) if y_band[0] <= v[1] <= y_band[1] and z_band[0] <= v[2] <= z_band[1])
    blocks, cur = [], [xs[0]] if xs else []
    for x in xs[1:]:
        if x - cur[-1] > 0.30:
            blocks.append((cur[0], cur[-1]))
            cur = []
        cur.append(x)
    if cur:
        blocks.append((cur[0], cur[-1]))
    return [max(1, round((b - a) / 0.46)) for a, b in blocks]


def letters(n):
    return [c for c in "ABCDEFGHJKL"][:n]   # no I, as on real seat maps


def rows_both_sides(tris, cams):
    """Rows counted across the aisle: seat-back z's from both window bands together, so a row with a seat on
    either side counts once and both sides share row numbers (as on real seat maps). Front first."""
    import statistics
    zs, per_side = [], {}
    for sign in (1, -1):
        side = [p for p in cams.values() if sign * p[0] > 0]
        if not side:
            continue
        lat = statistics.median(abs(p[0]) for p in side)
        y = statistics.median(p[1] for p in side)
        z_side = [v[2] for v in verts(tris) if lat - 0.8 <= sign * v[0] <= lat + 0.1 and y - 0.5 <= v[1] <= y + 0.05]
        per_side[sign] = len(rows_from_z(z_side))
        zs += z_side
    return rows_from_z(zs), per_side


def rows_from_z(zs):
    zs = sorted(zs)
    clusters, cur = [], []
    for z in zs:
        if cur and z - cur[-1] > 0.15:
            clusters.append(cur)
            cur = []
        cur.append(z)
    if cur:
        clusters.append(cur)
    return sorted(((min(c), max(c)) for c in clusters if len(c) >= 12), key=lambda r: -r[1])


def seat_map(cams, tris, wide=False):
    """cams: {slot: glTF pos}. Returns {slot: '12A' or note}."""
    out = {}
    right_letter = "F"
    if wide and tris:
        # count seats across in the main cabin, at the over-wing and wing views (the engine-front views can sit in
        # another cabin zone, ahead of door 2, where galleys and closets confuse the count)
        mid_cams = [cams[s] for s in "2367" if s in cams] or list(cams.values())
        ys = [p[1] for p in mid_cams]
        zs = [p[2] for p in mid_cams]
        mid = sum(zs) / len(zs)
        per = abreast(tris, (sum(ys) / len(ys) - 0.5, sum(ys) / len(ys)), (mid - 0.4, mid + 0.4))
        if sum(per) >= 7:
            right_letter = letters(sum(per))[-1]
        out["_abreast"] = "-".join(str(p) for p in per)
    rows, per_side = rows_both_sides(tris, cams)
    out["_rows"] = f"{len(rows)} rows (left side {per_side.get(1, 0)}, right side {per_side.get(-1, 0)})"
    for s, pos in cams.items():
        sign = 1 if pos[0] > 0 else -1
        if not rows:
            out[s] = "no seats"
            continue
        behind = [(i, r) for i, r in enumerate(rows) if r[1] <= pos[2] + 0.05]
        if not behind:
            out[s] = "ahead of row 1"
            continue
        i, r = behind[0]
        gap = pos[2] - r[1]
        label = f"{i + 1}{'A' if sign > 0 else right_letter}"
        out[s] = label + (" (extra legroom / exit area)" if gap > 0.9 else "")
    return out


def cams_of(path, eye_ft):
    eye = tuple(v * FT for v in eye_ft)
    return {k: v[0] for k, v in vc.read_cameras(path, eye).items() if k in "12345678"}


result, summary = {}, []

# ---------------- PMDG
from batch import RUNS  # noqa: E402
PM = [("777-200ER", "pmdg-aircraft-77er", "PMDG 777-200ER", "PMDG 777-200ER PW", 82.122316, -1.74, 7.722)] + list(RUNS)
SEATPAT = r"seat|ECOS|FCS|sofa|BR_|table"
pm_rep = {}
for lab, pkg, ac, preset, lon, lat, vert in PM:
    camfile = os.path.join(ROAM, ac, "presets", "pmdg", preset, "config", "cameras.CFG")
    cams = cams_of(camfile, (lon, lat, vert))
    if re.search(r"BCF|BDSF|777F", preset):
        smap = {s: "no seats (cargo deck)" for s in cams}
    else:
        pdir = os.path.join(C, pkg, "SimObjects", "Airplanes", ac, "presets", "pmdg", preset)
        parts, merged = vc.assemble(os.path.join(C, pkg), os.path.join(pdir, "config"), "interior", 0)
        mats = vc.node_mats(merged)
        tris = []
        centre = [sum(p[k] for p in cams.values()) / len(cams) for k in range(3)]
        for path, node, xml, off in parts:
            if re.search(SEATPAT, xml, re.I):
                p1 = path.replace("LOD0", "LOD1")
                vc.load_tris(p1 if os.path.exists(p1) else path, vc.attach_matrix(mats, node, off), 5, [(*centre, 40.0)], tris)
        if re.search(r"BBJ", preset):
            smap = {s: "VIP cabin (no numbered rows)" for s in cams}
        else:
            smap = seat_map(cams, tris, wide=ac.startswith("PMDG 777"))
    pm_rep[preset] = smap
    summary.append((preset, smap))
for f in glob.glob(os.path.join(ROAM, "PMDG *", "presets", "pmdg", "*", "config", "cameras.CFG")):
    preset = os.path.basename(os.path.dirname(os.path.dirname(f)))
    rep = preset if preset in pm_rep else preset.replace("SSW", "BW") if preset.replace("SSW", "BW") in pm_rep else None
    if rep is None and preset.startswith("PMDG 777-200ER"):
        rep = "PMDG 777-200ER PW"
    if rep:
        result[os.path.relpath(f, ROAM)] = pm_rep[rep]
    else:
        print("  ! no layout match for", preset)

# ---------------- Fenix (and FlyByWire from the Fenix A320's rows)
import fnxcheck as fx  # noqa: E402
FNX = {"FNX_319_CFM_SL_HD": "319", "FNX_319_CFM_SL_SD": "319", "FNX_320_CFM_SL": "320", "FNX_321_CFM_SL_SC": "321", "FNX_321_CFM_SL_TC": "321"}
fnx_rep, a320_tris = {}, None
for rep in FNX:
    camfile = os.path.join(ROAM, "FNX_32X", "presets", "fnx", rep, "config", "cameras.cfg")
    eye_m = fx.eye_for(rep)
    cams = cams_of(camfile, tuple(v / FT for v in eye_m))
    tris = []
    centre = [sum(p[k] for p in cams.values()) / len(cams) for k in range(3)]
    for L, A, name in fx.place(fx.assemble(rep, "interior")):
        if "Seats" in name:
            for f in L[min(3, len(L) - 1)]:
                vc.load_tris(f, A, 5, [(*centre, 40.0)], tris, fx.SKIP)
    smap = seat_map(cams, tris)
    fnx_rep[rep] = smap
    summary.append((rep, smap))
    if rep == "FNX_320_CFM_SL":
        a320_tris = tris
for f in glob.glob(os.path.join(ROAM, "FNX_32X", "presets", "fnx", "*", "config", "cameras.cfg")):
    p = os.path.basename(os.path.dirname(os.path.dirname(f))).split("_")
    rep = "_".join(["FNX", p[1], "CFM", "SL"] + p[4:])
    result[os.path.relpath(f, ROAM)] = fnx_rep[rep]
fbw_file = os.path.join(ROAM, "FlyByWire_A320_NEO", "cameras.CFG")
fbw_cams = cams_of(fbw_file, (43.72074, -1.723061, 4.355627))
# no seats in the FlyByWire: use the Fenix A320 rows (same airframe; datum within 5 cm), at the Fenix seat height
fx_y = 1.72
smap = seat_map({s: (p[0], fx_y, p[2]) for s, p in fbw_cams.items()}, a320_tris)
smap = {s: (v + " (Fenix A320 rows; no seats modelled)") for s, v in smap.items()}
result[os.path.relpath(fbw_file, ROAM)] = smap
summary.append(("FlyByWire_A320_NEO", smap))

# ---------------- iFly
import genclassic as gc  # noqa: E402
for variant in gc.IFLY_VARIANTS:
    camfile = os.path.join(ROAM, variant, "cameras.CFG")
    cams = cams_of(camfile, (49.683998, -1.63, 2.1))
    folder = os.path.join(gc.IFLY, variant, f"model.{gc.IFLY_VARIANTS[variant]}")
    cfg = open(os.path.join(folder, "model.CFG"), encoding="utf-8").read()
    intr = gc.model_file(os.path.normpath(os.path.join(folder, re.search(r"interior\s*=\s*(\S.*)", cfg).group(1).strip())))
    tris = []
    centre = [sum(p[k] for p in cams.values()) / len(cams) for k in range(3)]
    # economy seats are VC_CabinSeat_*, first class (166/178) is *CabinFirstClassSeat*; *Click* are click targets
    vc.load_tris(intr, None, 5, [(*centre, 40.0)], tris, r"^(?!.*(?:CabinSeat|FirstClassSeat))|Click")
    smap = seat_map(cams, tris)
    result[os.path.relpath(camfile, ROAM)] = smap
    summary.append((variant, smap))

json.dump(result, open(OUT, "w"), indent=1)
for name, smap in summary:
    print(f"{name:24s} " + "  ".join(f"{s}:{smap.get(s, '-').replace(' (Fenix A320 rows; no seats modelled)', '~')}" for s in "12345678")
          + (f"  | {smap['_rows']}" if "_rows" in smap else "") + (f"  abreast {smap['_abreast']}" if "_abreast" in smap else ""))
print(f"{len(result)} view files mapped -> {OUT}")
