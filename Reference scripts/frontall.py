"""Engine-front views (Alt+1/5) for the Boeing types and the iFly, by the same rule as front320.py: choose the window
by its angle off the inlet axis (target TARGET degrees, in the forward arc), then aim at the intake and keep the view
clear (ray-cast check). The PMDG 737s already sit at 45-52 degrees and are only measured here, not moved.
Rewrites only the slot 1 and 5 blocks of the listed files (InitialXyz, InitialPbh).
Usage: frontall.py [--only 777-200ER,iFly 189] [--target 55] [--write]
"""
import json, math, os, re, statistics, sys
S = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, S)
import viewcheck as vc  # noqa: E402
from batch import C  # noqa: E402
from gen737 import mesh_points, window_centers  # noqa: E402
from front320 import rewrite  # noqa: E402

ROAM = os.path.expandvars(r"%APPDATA%\Microsoft Flight Simulator 2024\SimObjects\Airplanes")
ZOOM_FALLBACK = 0.44
TARGET = float(sys.argv[sys.argv.index("--target") + 1]) if "--target" in sys.argv else 55.0
BAND = (50.0, 60.0)
OUT = os.path.join(S, "frontall.json")
WIN_PAT = r"^(cabin_windows|cabin_window_glass\d*|pax_window_glass|900ER_pax_window_glass)$"


def pmdg(label, pkg, ac, preset, eye_ft, lip, fan, axis, files, cam_lat=None, insets_override=None):
    eye = tuple(v * vc.FT for v in eye_ft)
    pdir = os.path.join(C, pkg, "SimObjects", "Airplanes", ac, "presets", "pmdg", preset)
    pts = []
    for path, node, xml, off in vc.assemble(os.path.join(C, pkg), os.path.join(pdir, "config"), "exterior", 0)[0]:
        pts += mesh_points(path, WIN_PAT)
    glass = statistics.median(abs(p[0]) for p in pts)
    cams = vc.read_cameras(os.path.join(ROAM, files[0]), eye)
    cur_lat = statistics.median(abs(cams[s][0][0]) for s in "1234")
    cam_y = statistics.median(cams[s][0][1] for s in "1234")

    def scene(pseudo):
        spheres = [(*c[0], 4.5) for c in pseudo.values()]
        parts, merged = vc.assemble(os.path.join(C, pkg), os.path.join(pdir, "config"), "interior", 0)
        mats = vc.node_mats(merged)
        tris = []
        for path, node, xml, off in parts:
            cls = 6 if re.search(r"cockpit|_VC", xml + path, re.I) else 5 if re.search(r"seat|ECOS|FCS|sofa|BR_|table", xml, re.I) else 4
            if cls in (5, 6) and "LOD0" in path and os.path.exists(path.replace("LOD0", "LOD1")):
                path = path.replace("LOD0", "LOD1")
            vc.load_tris(path, vc.attach_matrix(mats, node, off), cls, spheres, tris)
        etris = []
        for path, node, xml, off in vc.assemble(os.path.join(C, pkg), os.path.join(pdir, "config"), "exterior", 3)[0]:
            vc.load_tris(path, None, 3 if re.search(r"engine|eng[lr]_", path, re.I) else 2, [(*spheres[0][:3], 80.0)], etris)
        gy = min(t[5][1] for t in etris)
        return vc.Grid(tris, 0.12), vc.Grid(etris, 1.0), gy

    # around the current engine-front camera's own distance from the glass (the 200ER's other views sit deeper in)
    in1 = glass - abs(cams["1"][0][0])
    insets = sorted({round(max(0.08, in1 - 0.06), 2), round(in1, 2), round(in1 + 0.06, 2)}) if insets_override is None else insets_override
    return {"name": label, "eye": eye, "windows": {s: window_centers(pts, s) for s in "LR"}, "wall_x": glass, "insets": insets,
            "cam_y": cam_y, "lip": lip, "fan": fan, "axis": axis, "scene": scene, "files": [os.path.join(ROAM, f) for f in files],
            "zoom": cams["1"][4]}


def ifly(label, variants):
    import genclassic as gc
    ac = gc.ifly(variants[0])
    cams = vc.read_cameras(os.path.join(ROAM, variants[0], "cameras.CFG"), ac["eye"])
    cur_in = round(ac["wall_x"] - abs(cams["1"][0][0]), 2)
    return {"name": label, "eye": ac["eye"], "windows": ac["windows"], "wall_x": ac["wall_x"],
            "insets": sorted({round(max(0.08, cur_in - 0.04), 2), cur_in, round(cur_in + 0.06, 2)}), "cam_y": cams["1"][0][1],
            "lip": 4.43, "fan": 4.17, "axis": (4.89, -1.76), "scene": ac["scene"],
            "files": [os.path.join(ROAM, v, "cameras.CFG") for v in variants], "zoom": cams["1"][4]}


ADAPTERS = {
    "777-200ER": lambda: pmdg("777-200ER", "pmdg-aircraft-77er", "PMDG 777-200ER", "PMDG 777-200ER PW", (82.122316, -1.74, 7.722),
                              6.96, 5.44, (9.69, -1.30), [rf"PMDG 777-200ER\presets\pmdg\PMDG 777-200ER {e}\config\cameras.CFG" for e in ("PW", "GE", "RR")]),
    "777-300ER": lambda: pmdg("777-300ER", "pmdg-aircraft-77w", "PMDG 777-300ER", "PMDG 777-300ER", (99.559998, -1.74, 7.722),
                              7.39, 5.90, (9.66, -1.22), [r"PMDG 777-300ER\presets\pmdg\PMDG 777-300ER\config\cameras.CFG"]),
    # PMDG 737 cabins: the generated engine-front cameras sat 30 cm in from the glass (the sim showed the wall between
    # two windows); search close to the glass. SSW presets share the BW cabin. Engine: CFM56-7B, same datum on all three.
    **{p: (lambda p=p, fam=fam, pkg=pkg, eye=eye: pmdg(p, pkg, f"PMDG {fam}", p, eye, 3.01, 2.77, (4.86, -0.85),
                                                       [rf"PMDG {fam}\presets\pmdg\{q}\config\cameras.CFG" for q in (p, p.replace(" BW", " SSW"))],
                                                       insets_override=(0.08, 0.12, 0.16)))
       for fam, pkg, eye, presets in (
           ("737-700", "pmdg-aircraft-737", (37.31212336, -1.66, 3.909), ("PMDG 737-700 BW TC", "PMDG 737-BBJ BW", "PMDG 737-700 BW SC")),
           ("737-800", "pmdg-aircraft-738", (47.07464336, -1.66, 3.909), ("PMDG 737-800 BW HD", "PMDG 737-800 BW SC", "PMDG 737-800 BW TC", "PMDG 737-BBJ2 BW")),
           ("737-900", "pmdg-aircraft-739", (52.13864336, -1.66, 3.909), ("PMDG 737-900 BW SC", "PMDG 737-900 BW TC", "PMDG 737-900ER BW HD",
                                                                          "PMDG 737-900ER BW SC", "PMDG 737-900ER BW TC")))
       for p in presets},
    # each iFly cabin separately: the 166/178 have first-class seats in the front rows
    "iFly 189": lambda: ifly("iFly 189", ["iFly 737-MAX8-189Seats"]),
    "iFly 178": lambda: ifly("iFly 178", ["iFly 737-MAX8"]),
    "iFly 166": lambda: ifly("iFly 166", ["iFly 737-MAX8-166Seats"]),
    "iFly 8200": lambda: ifly("iFly 8200", ["iFly 737-MAX8200"]),
}


def run(ac):
    eye = ac["eye"]
    zoom = ac.get("zoom", ZOOM_FALLBACK)
    rel = lambda p: [p[0] - eye[1], p[1] - eye[2], p[2] - eye[0]]
    cands = {}
    for s, side, sign in (("1", "L", -1), ("5", "R", 1)):
        reach = 1.25 * math.hypot(ac["axis"][0] - ac["wall_x"], ac["cam_y"] - ac["axis"][1])
        zs = [z for z in ac["windows"][side] if ac["lip"] - 0.6 <= z <= ac["lip"] + reach]
        cands[s] = [(sign * (ac["wall_x"] - ins), ac["cam_y"], z) for z in zs for ins in ac["insets"]]
    pts = [p for c in cands.values() for p in c]
    pseudo = {str(i): vc.camera(tuple(rel(p)), (0, 0), eye, zoom) for i, p in enumerate(pts)}
    gin, gext, gy = ac["scene"](pseudo)

    def evaluate(xyz, pbh, w=32, h=18):
        cam = vc.camera(tuple(xyz), (math.radians(pbh[0]), math.radians(pbh[2])), eye, zoom)
        img, counts, core = vc.render(cam, gin, gext, gy, w, h)
        tot, ctot = sum(counts), sum(core)
        return (100 * (counts[7] + counts[8]) / tot, 100 * sum(core[k] for k in (0, 1, 2, 3)) / ctot,
                100 * (core[2] + core[3]) / ctot, 100 * core[3] / ctot, img[h // 2][w // 2], img)

    aim_z = (ac["lip"] + ac["fan"]) / 2
    chosen, report, cand_log = {}, [], {}
    for s, sign in (("1", -1), ("5", 1)):
        rows = []
        for p in cands[s]:
            lat = ac["axis"][0] - abs(p[0])
            hdg0 = 90 + math.degrees(math.atan2(p[2] - aim_z, lat))
            pit0 = -math.degrees(math.atan2(p[1] - ac["axis"][1], math.hypot(lat, p[2] - aim_z)))
            best = None
            for dh in (-10, -5, 0, 6, 12):
                for dp in (0, 5):
                    pbh = (round(pit0 + dp, 2), 0.0, round(sign * (hdg0 + dh), 2))
                    bad, out, wing, eng, center, _ = evaluate(rel(p), pbh)
                    ok = bad <= 5 and center not in (7, 8)
                    sc = (2.0 * eng + 0.3 * wing + 0.2 * out - 3 * bad) if ok else -1000 - bad
                    if best is None or sc > best[0]:
                        best = (sc, pbh, bad, out, wing, eng, center)
            radial = math.hypot(lat, ac["cam_y"] - ac["axis"][1])
            rows.append((p, math.degrees(math.atan2(radial, p[2] - ac["lip"])), best))
        valid = [r for r in rows if r[2][0] > -1000 and r[2][5] >= 10 and r[2][6] in (0, 1, 2, 3)]
        band = [r for r in valid if BAND[0] <= r[1] <= BAND[1]]
        pick = max(band, key=lambda r: r[2][0]) if band else min(valid, key=lambda r: (abs(r[1] - TARGET), -r[2][0])) if valid else None
        cand_log[s] = [{"z": p[2], "x": p[0], "angle": round(a, 1), "pbh": list(b[1]), "score": round(b[0], 1), "bad": round(b[2], 1),
                        "outside": round(b[3], 1), "engine": round(b[5], 1), "centre": vc.NAMES[b[6]]} for p, a, b in rows]
        for p, ang, b in sorted(rows, key=lambda r: (-r[0][2], abs(r[0][0]))):
            mark = " <== chosen" if pick and p == pick[0] else ""
            report.append(f"  Alt+{s} z {p[2]:+.2f} ({p[2] - ac['lip']:+.2f} m vs lip), {ac['wall_x'] - abs(p[0]):.2f} m in: "
                          f"{ang:4.1f} deg off the inlet axis | hdg {b[1][2]:+.0f} pitch {b[1][0]:+.0f}: outside {b[3]:.0f}% "
                          f"wing/engine {b[4]:.0f}% engine {b[5]:.0f}% bad {b[2]:.0f}% centre {vc.NAMES[b[6]]}{mark}")
        if pick:
            p, ang, b = pick
            _, _, _, _, _, img = evaluate(rel(p), b[1], 96, 54)
            os.makedirs(os.path.join(S, "vc", "frontall"), exist_ok=True)
            vc.write_png(os.path.join(S, "vc", "frontall", f"{ac['name'].replace(' ', '_')}_view_{s}.png"), img)
            chosen[s] = {"xyz": [round(v, 6) for v in rel(p)], "pbh": list(b[1]), "z": p[2], "angle": ang,
                         "ahead_of_lip": p[2] - ac["lip"], "engine_pct": b[5], "outside_pct": b[3], "bad_pct": b[2]}
    chosen["_candidates"] = cand_log
    return chosen, report


if __name__ == "__main__":
    only = sys.argv[sys.argv.index("--only") + 1].split(",") if "--only" in sys.argv else list(ADAPTERS)
    results = json.load(open(OUT)) if os.path.exists(OUT) else {}
    for name in only:
        ac = ADAPTERS[name]()
        chosen, report = run(ac)
        print(f"== {name}: inlet lip z {ac['lip']:+.2f}, fan {ac['fan']:+.2f}, axis |x| {ac['axis'][0]:.2f} y {ac['axis'][1]:+.2f}, "
              f"glass |x| {ac['wall_x']:.3f}, cam y {ac['cam_y']:+.2f}, insets {ac['insets']}, target {TARGET:.0f} deg")
        print("\n".join(report), flush=True)
        results[name] = chosen
        json.dump(results, open(OUT, "w"), indent=1)
        views = {k: v for k, v in chosen.items() if k in ("1", "5")}
        if "--write" in sys.argv and len(views) == 2:
            for f in ac["files"]:
                print(f"    wrote {os.path.relpath(f, ROAM)}: {rewrite(f, views)}")
