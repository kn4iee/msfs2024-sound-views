"""Re-place the A320-family engine-front views (Alt+1/5) clearly in front of the intake.

Why: the first search rewarded seeing more engine, which pulled these seats back beside the intake
(Fenix A319/A320 1.4 m ahead of the lip, A321 0.3 m, FlyByWire 0.6 m; the PMDG 737s sit about 3.1 m ahead).
Rule here: pick the window by its angle to the inlet first, then aim. The angle is measured from the engine's
forward axis to the line from the inlet lip to the camera, including the height difference. Inlet-radiated fan
and buzzsaw noise is strongest in the forward arc, roughly 40-60 degrees off the inlet axis; the target is 55.
Then aim at the intake (between lip and fan) and keep the view clear (ray-cast check).
Rewrites only the slot 1 and 5 blocks (InitialXyz, InitialPbh); everything else stays byte-for-byte.
Usage: front320.py [--only FNX_320_CFM_SL,FBW] [--write]
"""
import json, math, os, re, statistics, sys
S = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, S)
import viewcheck as vc  # noqa: E402
import fnxcheck as fx  # noqa: E402
from gen737 import mesh_points  # noqa: E402

ROAM = os.path.expandvars(r"%APPDATA%\Microsoft Flight Simulator 2024\SimObjects\Airplanes")
ZOOM = 0.354
TARGET = 55.0
BAND = (50.0, 60.0)
OUT = os.path.join(S, "front320.json")
LAYOUTS = ["FNX_320_CFM_SL", "FNX_319_CFM_SL_HD", "FNX_319_CFM_SL_SD", "FNX_321_CFM_SL_SC", "FNX_321_CFM_SL_TC", "FBW"]


def fenix(rep):
    win, glass_x = fx.windows(rep)
    # engine (CFM, left; the IAE twins' lip is 5 cm further forward and their fan closer to the lip)
    return {"name": rep, "eye": fx.eye_for(rep), "windows": win, "wall_x": glass_x, "insets": (0.08, 0.10, 0.15), "cam_y": 1.72,
            "lip": 2.18, "fan": 1.29, "axis": (5.70, -0.96),
            "scene": lambda pseudo: fx.scene(rep, pseudo, radius=3.6, verbose=False),
            "files": [os.path.join(ROAM, "FNX_32X", "presets", "fnx", p, "config", "cameras.cfg") for p in twins(rep)]}


def twins(rep):
    p = rep.split("_")
    return ["_".join(["FNX", p[1], e, w] + p[4:]) for e in ("CFM", "IAE") for w in ("SL", "WF")]


def fbw():
    import genclassic as gc
    ac = gc.fbw("FlyByWire_A320_NEO")
    ext = os.path.join(gc.FBW, "A320_NEO_LOD00.gltf")
    rl = [p for p in mesh_points(ext, r"^REACTOR_LEFT$")]
    fan = [p for p in mesh_points(ext, r"^PROP_.*") if p[0] > 0]
    ys = [p[1] for p in rl]
    return {"name": "FBW", "eye": ac["eye"], "windows": ac["windows"], "wall_x": ac["wall_x"], "insets": (0.06, 0.08, 0.11, 0.14),
            "cam_y": ac["cam_y"], "lip": max(p[2] for p in rl), "fan": max(p[2] for p in fan) if fan else max(p[2] for p in rl) - 0.9,
            "axis": (statistics.median(p[0] for p in rl), (min(ys) + max(ys)) / 2), "scene": ac["scene"],
            "files": [os.path.join(ROAM, "FlyByWire_A320_NEO", "cameras.CFG")]}


def off_axis(ac, x_abs, z):
    lat = ac["axis"][0] - x_abs
    radial = math.hypot(lat, ac["cam_y"] - ac["axis"][1])
    return math.degrees(math.atan2(radial, z - ac["lip"]))


def run(ac):
    eye = ac["eye"]
    rel = lambda p: [p[0] - eye[1], p[1] - eye[2], p[2] - eye[0]]
    cands = {}
    for s, side, sign in (("1", "L", -1), ("5", "R", 1)):
        zs = [z for z in ac["windows"][side] if ac["lip"] + 0.2 <= z <= ac["lip"] + 4.6]   # from the current seats forward
        cands[s] = [(sign * (ac["wall_x"] - ins), ac["cam_y"], z) for z in zs for ins in ac["insets"]]
    pts = [p for c in cands.values() for p in c]
    pseudo = {str(i): vc.camera(tuple(rel(p)), (0, 0), eye, ZOOM) for i, p in enumerate(pts)}
    gin, gext, gy = ac["scene"](pseudo)

    def evaluate(xyz, pbh, w=32, h=18):
        cam = vc.camera(tuple(xyz), (math.radians(pbh[0]), math.radians(pbh[2])), eye, ZOOM)
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
            ang = off_axis(ac, abs(p[0]), p[2])
            rows.append((p, ang, best))
        # a usable engine-front view: nothing blocking, the centre looking outside, and at least 10% engine in the middle half;
        # inside the 50-60 degree band take the clearest view of the engine, otherwise the angle nearest the target
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
            os.makedirs(os.path.join(S, "vc", "front320"), exist_ok=True)
            vc.write_png(os.path.join(S, "vc", "front320", f"{ac['name']}_view_{s}.png"), img)
            chosen[s] = {"xyz": [round(v, 6) for v in rel(p)], "pbh": list(b[1]), "z": p[2], "angle": ang,
                         "ahead_of_lip": p[2] - ac["lip"], "engine_pct": b[5], "outside_pct": b[3], "bad_pct": b[2]}
    chosen["_candidates"] = cand_log
    return chosen, report


def rewrite(path, views):
    text = open(path, "rb").read().decode("utf-8")
    for s, v in views.items():
        m = re.search(r'\[CAMERADEFINITION\.\d+\]\r?\nTitle="%s".*?(?=\[CAMERADEFINITION|\Z)' % s, text, re.S)
        blk = re.sub(r"InitialXyz=\s*[^\r\n]+", "InitialXyz= {:.6f}, {:.6f}, {:.6f}".format(*v["xyz"]), m.group(0))
        blk = re.sub(r"InitialPbh=\s*[^\r\n]+", "InitialPbh= {:.6f}, {:.6f}, {:.6f}".format(*v["pbh"]), blk)
        text = text[:m.start()] + blk + text[m.end():]
    open(path, "wb").write(text.encode("utf-8"))
    chk = open(path, "rb").read()
    return f"{chk.count(b'[CAMERADEFINITION.')} blocks, CRLF {chk.count(bytes([13, 10]))}/{chk.count(bytes([10]))}"


if __name__ == "__main__":
    only = sys.argv[sys.argv.index("--only") + 1].split(",") if "--only" in sys.argv else LAYOUTS
    results = json.load(open(OUT)) if os.path.exists(OUT) else {}
    for name in only:
        ac = fbw() if name == "FBW" else fenix(name)
        chosen, report = run(ac)
        print(f"== {name}: inlet lip z {ac['lip']:+.2f}, fan face {ac['fan']:+.2f}, engine axis |x| {ac['axis'][0]:.2f} y {ac['axis'][1]:+.2f}")
        print("\n".join(report), flush=True)
        results[name] = chosen
        json.dump(results, open(OUT, "w"), indent=1)
        views = {k: v for k, v in chosen.items() if k in ("1", "5")}
        if "--write" in sys.argv and len(views) == 2:
            for f in ac["files"]:
                print(f"    wrote {os.path.relpath(f, ROAM)}: {rewrite(f, views)}")
