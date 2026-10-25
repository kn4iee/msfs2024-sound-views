"""Sound-tuned views for the BlueBird Simulations 757-200 (10 variants, one model per variant folder).

Usage: gen757.py [--only <variant>[,<variant>...]] [--out <dir>] [--write] [--from-cache]
Same layout and seat search as the single-model aircraft (genviews.search), then the engine-front views (Alt+1/5)
are re-chosen by angle off the inlet axis (frontall.run). Three searches (rr-nw, rr-AWE, pw); the other variants copy
one of them (SAME_AS). Old view files are replaced only with --write.

Frame: unlike the other aircraft here, the 757's reference datum is not the model origin. flight_model.cfg puts it
86.81667 ft ahead of the model centre (MSFS SDK: "the position of the Datum Reference Point relative to the model
center"), about 4 m ahead of the nose, and the eyepoint is -20.66667 ft from it. So eye = 66.15 ft forward of the
model origin; the pack's own pilot camera then lands above the captain's seat, 0.3 m behind the yoke.
"""
import json, os, re, struct, sys, time
sys.path.insert(0, os.path.dirname(__file__))
import viewcheck as vc  # noqa: E402
import genviews as gv  # noqa: E402
import genclassic as gc  # noqa: E402
import frontall as fa  # noqa: E402

C = r"D:\MSFS2024 Community\Community"
PKG = os.path.join(C, r"bluebirdsim-aircraft-757-200\SimObjects\Airplanes")
ROAM = os.path.expandvars(r"%APPDATA%\Microsoft Flight Simulator 2024\SimObjects\Airplanes")
OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else os.path.join(os.path.dirname(__file__), "vc", "b757")
FT = vc.FT
DATUM_FT = 86.81667
EYE = ((DATUM_FT - 20.66667) * FT, -2 * FT, 4.6 * FT)
PILOT = ((0.08, 0.22, -0.08), (-16.0, 0.0, 0.0), 0.57)   # the pack's own "Pilot" camera
SKIP = r"collision|occluder|drone|glass|window_?pane|Cover|SafetyCone|Chock|CLICK|Mouse|^Soundnode|^sound_"
# ground service vehicles and stairs, engine covers, ice and streak overlays: not part of the airframe in flight
SKIP_MATS = r"SVC1|GNDSVC|FUEL_TRUCK|CATER_TRUCK|BAGGAGE_LOADER|GROUND_SVC|COVERS|FROST|intake streaks|glass|windshield|invisible"
ENGINE_MATS = r"^(EnginesMain|EngineLivery|EnginesExtra|fanblurred|BBS757_PW_ENG_EXTERIOR|BBS757_PW_ENG_INTERIOR|PW_EngineLivery)$"
WINDOW_GLASS = r"^Cabin_innerGLASS$"     # the cabin side of each window; one pane per window
# variant folder: (exterior model, its cabin's interior model for each engine, engine)
STD = {"PW": r"bbs-757-200-pw\model\BBS_752_PW_INTERIOR.gltf", "RR": r"bbs-757-200-rr\model\BBS_752_RR_INTERIOR.gltf"}
AWE = {"PW": r"bbs-757-200-pw-AWE\model\BBS_752_PW_INTERIOR_AWE.gltf", "RR": r"bbs-757-200-rr-AWE\model\BBS_752_RR_INTERIOR_AWE.gltf"}
NOCAB = {"PW": r"bbs-757-200-pw\model.nocab\BBS_752_PW_INTERIOR_NC.gltf"}
VARIANTS = {
    "bbs-757-200-pw": (r"bbs-757-200-pw\model\BBS_752_PW.gltf", STD, "PW"),
    "bbs-757-200-pw-nw": (r"bbs-757-200-pw-nw\model\BBS_752_PW_NW.gltf", STD, "PW"),
    "bbs-757-200-pw-AWE": (r"bbs-757-200-pw\model\BBS_752_PW.gltf", AWE, "PW"),
    "bbs-757-200-pw-nw-AWE": (r"bbs-757-200-pw-nw\model\BBS_752_PW_NW.gltf", AWE, "PW"),
    "bbs-757-200-pw-NC": (r"bbs-757-200-pw\model\BBS_752_PW.gltf", NOCAB, "PW"),
    "bbs-757-200-rr-nw": (r"bbs-757-200-rr-nw\model\BBS_752_RR_NW.gltf", STD, "RR"),
    "bbs-757-200-rr": (r"bbs-757-200-rr\model\BBS_752_RR.gltf", STD, "RR"),
    "bbs-757-200-rr-scimitarw": (r"bbs-757-200-rr-scimitarw\model\BBS_752_RR_SCIMITARW.gltf", STD, "RR"),
    "bbs-757-200-rr-AWE": (r"bbs-757-200-rr\model\BBS_752_RR.gltf", AWE, "RR"),
    "bbs-757-200-rr-nw-AWE": (r"bbs-757-200-rr-nw\model\BBS_752_RR_NW.gltf", AWE, "RR"),
}

# twins take the searched variant's views: the wingtip changes no seat, the no-cabin model has the same fuselage, and
# the four-door cabin's search (rr-AWE) came out within 0.1 mm of the standard cabin's (its third door is aft of every
# view), so the PW four-door versions take the PW standard views without a search of their own
SAME_AS = {"bbs-757-200-rr": "bbs-757-200-rr-nw", "bbs-757-200-rr-scimitarw": "bbs-757-200-rr-nw",
           "bbs-757-200-rr-nw-AWE": "bbs-757-200-rr-AWE", "bbs-757-200-pw-nw": "bbs-757-200-pw",
           "bbs-757-200-pw-AWE": "bbs-757-200-pw", "bbs-757-200-pw-nw-AWE": "bbs-757-200-pw",
           "bbs-757-200-pw-NC": "bbs-757-200-pw"}

_orig_mat_class = vc.mat_class


def mat_class(g, mi):
    if mi is not None and re.search(SKIP_MATS, g["materials"][mi].get("name", ""), re.I):
        return "skip", False
    return _orig_mat_class(g, mi)


vc.mat_class = mat_class
gc.BASE_SKIP = SKIP


def points(path, node_pat=None, mat_pat=None):
    """World-space vertices of mesh primitives matching a node and/or material pattern. Unlike gen737.mesh_points this
    honours ASOBO_primitive ranges: the BlueBird models share vertex buffers between primitives."""
    g, nodes, world = vc.load_gltf(path)
    files, out = {}, []

    def fileof(b):
        if b not in files:
            files[b] = open(os.path.join(os.path.dirname(path), g["buffers"][b]["uri"]), "rb")
        return files[b]
    for i, n in enumerate(nodes):
        if "mesh" not in n or (node_pat and not re.search(node_pat, n.get("name", ""), re.I)):
            continue
        W = world(i)
        for p in g["meshes"][n["mesh"]]["primitives"]:
            mi = p.get("material")
            if mat_pat and (mi is None or not re.search(mat_pat, g["materials"][mi].get("name", ""), re.I)):
                continue
            acc, ia = g["accessors"][p["attributes"]["POSITION"]], g["accessors"][p["indices"]]
            bv, ibv = g["bufferViews"][acc["bufferView"]], g["bufferViews"][ia["bufferView"]]
            ap = p.get("extras", {}).get("ASOBO_primitive", {})
            code, size = {5121: ("B", 1), 5123: ("H", 2), 5125: ("I", 4)}[ia["componentType"]]
            f = fileof(ibv["buffer"])
            f.seek(ibv.get("byteOffset", 0) + ia.get("byteOffset", 0))
            idx = struct.unpack("<%d%s" % (ia["count"], code), f.read(ia["count"] * size))
            start = ap.get("StartIndex", 0)
            used = sorted(set(idx[start:start + ap.get("PrimitiveCount", (len(idx) - start) // 3) * 3]))
            f = fileof(bv["buffer"])
            for k in used:
                f.seek(bv.get("byteOffset", 0) + acc.get("byteOffset", 0) + (ap.get("BaseVertexIndex", 0) + k) * bv.get("byteStride", 12))
                out.append(vc.xf(W, struct.unpack("<3f", f.read(12))))
    return out


def names_with_material(path, mat_pat):
    g = json.load(open(path, encoding="utf-8"))
    return sorted({n.get("name", "") for n in g["nodes"] if "mesh" in n and any(
        "material" in p and re.search(mat_pat, g["materials"][p["material"]].get("name", ""), re.I) for p in g["meshes"][n["mesh"]]["primitives"])})


def window_rows(pts):
    """Window centres along the cabin, per side, from the panes' vertices (0.51 m pitch, 0.28 m wide panes), and the
    median pane-centre height (each pane's vertices bunch at its lower edge, so not the median vertex)."""
    import statistics
    rows, mids = {}, []
    for s, sign in (("L", 1), ("R", -1)):
        sel = sorted((p for p in pts if sign * p[0] > 1.5), key=lambda p: p[2])
        groups, cur = [], []
        for p in sel:
            if cur and p[2] - cur[-1][2] > 0.12:
                groups.append(cur)
                cur = []
            cur.append(p)
        groups += [cur] if cur else []
        rows[s] = [(min(q[2] for q in g) + max(q[2] for q in g)) / 2 for g in groups]
        mids += [(min(q[1] for q in g) + max(q[1] for q in g)) / 2 for g in groups]
    return rows, statistics.median(mids)


def engine(ext):
    """Inlet lip (forward-most nacelle z), fan face and the engine axis (|x|, y) of the left engine."""
    nac = [p for p in points(ext, mat_pat=ENGINE_MATS) if p[0] > 0]
    lip = max(p[2] for p in nac)
    ring = [p for p in nac if p[2] > lip - 0.15]
    fan = [p for p in points(ext, mat_pat=r"^fanblurred$") if p[0] > 0]
    axis = ((min(p[0] for p in ring) + max(p[0] for p in ring)) / 2, (min(p[1] for p in ring) + max(p[1] for p in ring)) / 2)
    return lip, max(p[2] for p in fan), axis


def wing_root(ext):
    """Root leading and trailing edge: wing vertices just outboard of the fuselage (|x| 1.9-2.6)."""
    w = [p for p in points(ext, mat_pat=r"^BBS757wingleft$") if 1.9 <= p[0] <= 2.6]
    return max(p[2] for p in w), min(p[2] for p in w)


def adapter(variant):
    ext_rel, cabins, eng = VARIANTS[variant]
    ext = os.path.join(PKG, ext_rel)
    intr = os.path.join(PKG, cabins[eng])
    glass_src = intr if cabins is not NOCAB else os.path.join(PKG, STD[eng])   # no cabin: the same fuselage and windows
    pts = points(glass_src, mat_pat=WINDOW_GLASS)
    import statistics
    win, win_y = window_rows(pts)
    wall_x = statistics.median(abs(p[0]) for p in pts if abs(p[0]) > 1.5)
    lip, fan, axis = engine(ext)
    le, te = wing_root(ext)
    eng_names = names_with_material(ext, ENGINE_MATS)
    engine_pat = "^(?:" + "|".join(re.escape(n) for n in eng_names) + ")$"
    ws = [p for p in points(intr, node_pat=r"^WINDSHIELD_GLASS_L$") if p[0] > 0]
    print(f"{variant}: {os.path.basename(ext)} + {os.path.basename(intr)}; {len(win['L'])}/{len(win['R'])} windows, glass |x| {wall_x:.3f}, "
          f"window centre y {win_y:.3f}; {eng} inlet lip z {lip:+.2f}, fan {fan:+.2f}, axis |x| {axis[0]:.2f} y {axis[1]:+.2f}; "
          f"wing root LE {le:+.2f} TE {te:+.2f}", flush=True)
    tag = variant.replace("bbs-757-200-", "")
    # one scene load per run: the seat search and the engine-front search (front()) both ask for one, so the first
    # load also covers every window the engine-front search can try (the same z range as frontall.run)
    load, cache = gc.classic_scene([intr], [ext], engine_pat), []
    reach = 1.25 * ((axis[0] - wall_x) ** 2 + (win_y + 0.03 - axis[1]) ** 2) ** 0.5
    extra = [vc.camera((sign * (wall_x - 0.1) - EYE[1], win_y + 0.03 - EYE[2], z - EYE[0]), (0, 0), EYE, gv.ZOOM)
             for side, sign in (("L", -1), ("R", 1)) for z in win[side] if lip - 0.6 <= z <= lip + reach]

    def scene(pseudo):
        if not cache:
            cache.append(load({**pseudo, **{f"front{i}": c for i, c in enumerate(extra)}}))
        return cache[0]
    return {"eye": EYE, "windows": win, "wall_x": wall_x, "insets": (0.10, 0.16, 0.22, 0.30), "cam_y": win_y + 0.03,
            # over-wing 1 m behind the root leading edge; wing over the L/R hydraulic pumps (z -0.64) and the main gear,
            # mid-way along the root; behind the wing 2 m behind the root trailing edge
            "roles": {"front": (lip + 3.8, -25.0, 125.0), "overwing": (le - 1.0, -14.0, 92.0), "wing": (-0.9, -13.0, 78.0),
                      "roar": (te - 2.0, -12.0, 68.0)},
            "scene": scene, "pilot": PILOT,
            "windshield_pts": ws, "png_dir": os.path.join(OUT, tag), "dst": os.path.join(ROAM, variant, "cameras.CFG"),
            "lip": lip, "fan": fan, "axis": axis, "engine": eng, "le": le, "te": te}


def front(ac, variant):
    """Alt+1/5 by angle off the inlet axis (50-60 degrees, nearest 55), aimed between lip and fan, 8-14 cm from the glass."""
    fa.S = OUT
    fac = {"name": variant, "eye": ac["eye"], "windows": ac["windows"], "wall_x": ac["wall_x"], "insets": (0.08, 0.11, 0.14),
           "cam_y": ac["cam_y"], "lip": ac["lip"], "fan": ac["fan"], "axis": ac["axis"], "scene": ac["scene"], "zoom": gv.ZOOM}
    chosen, report = fa.run(fac)
    print("\n".join(report), flush=True)
    return {s: (chosen[s]["xyz"], tuple(chosen[s]["pbh"]), gv.ZOOM) for s in ("1", "5") if s in chosen}


def seats(variant, views):
    """Seat label (12A) for each cabin view, as in seatrows.py: rows are clusters of seat-back vertices in the window
    band, front first; a camera gets the row whose seat back is just behind it. Unlike seatrows.py, each side is
    clustered on its own (the first-class seats are staggered 0.4 m across the aisle, so pooled they merge into one row),
    then a row on one side is paired with the row beside it on the other (centres within 0.6 m; economy rows are 0.75 m
    or more apart) and a row with no partner counts once, as on a seat map: the four-door cabin has a right-only row at
    door 2. Economy seats use CABIN_ECONSEATS*, first class the Cabin Busclass2 mesh."""
    import statistics
    ext_rel, cabins, eng = VARIANTS[variant]
    if cabins is NOCAB:
        return {s: "no seats (no cabin)" for s in "12345678"}
    cams = {s: vc.camera(tuple(views[s][0]), (0, 0), EYE, gv.ZOOM)[0] for s in "12345678"}
    pts = points(os.path.join(PKG, cabins[eng]), mat_pat=r"^(CABIN_ECONSEATS(_0[12])?|Cabin Busclass2)$")
    rows, out = {}, {}
    for sign in (1, -1):
        side = [p for p in cams.values() if sign * p[0] > 0]
        lat, y = statistics.median(abs(p[0]) for p in side), statistics.median(p[1] for p in side)
        zs = sorted(v[2] for v in pts if lat - 0.8 <= sign * v[0] <= lat + 0.1 and y - 0.5 <= v[1] <= y + 0.05)
        clusters, cur = [], []
        for z in zs:
            if cur and z - cur[-1] > 0.15:
                clusters.append(cur)
                cur = []
            cur.append(z)
        clusters += [cur] if cur else []
        rows[sign] = sorted(((min(c), max(c)) for c in clusters if len(c) >= 12), key=lambda r: -r[1])
    centre = lambda r: (r[0] + r[1]) / 2
    union = [[centre(r), {1: r}] for r in rows[1]]
    for r in rows[-1]:
        free = [u for u in union if -1 not in u[1] and abs(u[0] - centre(r)) < 0.6]
        if free:
            min(free, key=lambda u: abs(u[0] - centre(r)))[1][-1] = r
        else:
            union.append([centre(r), {-1: r}])
    union.sort(key=lambda u: -u[0])
    number = {(sign, r): i + 1 for i, u in enumerate(union) for sign, r in u[1].items()}
    out["_rows"] = f"{len(union)} rows ({len(rows[1])} with a left window seat, {len(rows[-1])} with a right one)"
    for s, p in cams.items():
        sign = 1 if p[0] > 0 else -1
        # the band runs from the seat back to the front of the cushion, so a camera inside it sits in that row
        # (seatrows.py tests the band's front, which would put a camera inside a 1.2 m first-class seat in the row behind)
        behind = [r for r in rows[sign] if r[0] <= p[2] + 0.05]
        if not behind:
            out[s] = "ahead of row 1"
            continue
        r = behind[0]
        out[s] = f"{number[(sign, r)]}{'A' if sign > 0 else 'F'}" + (" (extra legroom / exit area)" if p[2] - r[1] > 0.9 else "")
    return out


if __name__ == "__main__":
    variants = sys.argv[sys.argv.index("--only") + 1].split(",") if "--only" in sys.argv else list(VARIANTS)
    for v in variants:
        ac = adapter(v)
        cache = os.path.join(ac["png_dir"], "views.json")
        if v in SAME_AS:
            cache = os.path.join(OUT, SAME_AS[v].replace("bbs-757-200-", ""), "views.json")
            views = {k: tuple(x) for k, x in json.load(open(cache)).items()}
            print(f"    same views as {SAME_AS[v]}", flush=True)
        elif "--from-cache" in sys.argv:
            views = {k: tuple(x) for k, x in json.load(open(cache)).items()}
        else:
            t0 = time.time()
            views, notes = gv.search(ac)
            print(f"{v}  ({time.time() - t0:.0f}s)\n" + "\n".join(notes), flush=True)
            views.update(front(ac, v))
            json.dump(views, open(cache, "w"), indent=1)
        if "--write" in sys.argv:
            os.makedirs(os.path.dirname(ac["dst"]), exist_ok=True)
            open(ac["dst"], "w", encoding="utf-8", newline="\r\n").write(gv.camera_file(views))
        print(f"    {'wrote' if '--write' in sys.argv else 'would write'} {ac['dst']}", flush=True)
