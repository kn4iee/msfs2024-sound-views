"""Generate sound-tuned custom views for every Fenix A319/A320/A321 preset (same layout as the PMDG sets).

Slots: 1/5 engine front, 2/6 over-wing (slats), 3/7 wing over the main gear bay, 4/8 behind the wing
(roar); 1-4 left, 5-8 right. 9 = the pilot view already saved on each type, 0 = windshield GoPro.
Targets come from the Fenix models (datum = model origin; wing, engines and gear sit at the same datum
z on all three types). Each slot is chosen by ray-cast scoring among the nearest windows and insets.
One search per cabin layout; engine (CFM/IAE) and wingtip (SL/WF) twins get the same views.

Usage: genfnx.py [--write] [--only FNX_320_CFM_SL,...]
"""
import json, math, os, re, sys, time
sys.path.insert(0, os.path.dirname(__file__))
import viewcheck as vc  # noqa: E402
import fnxcheck as fx  # noqa: E402
from gen737 import mesh_points, windshield_z, block  # noqa: E402

ROAM = os.path.expandvars(r"%APPDATA%\Microsoft Flight Simulator 2024\SimObjects\Airplanes\FNX_32X\presets\fnx")
OUT = os.path.join(os.path.dirname(__file__), "vc", "fnx_new")
ZOOM = 0.354
CAM_Y = 1.72                       # head height (datum frame, m); window centre is 1.69
INSETS = (0.10, 0.15, 0.25, 0.35, 0.45)  # m in from the outer glass
# role: (target datum z, pitch, heading magnitude); left heading negative
ROLES = {"front": (4.4, -25.0, 115.0), "overwing": (-0.57, -14.0, 92.0), "wing": (-4.6, -13.0, 75.0), "roar": (-7.8, -12.0, 68.0)}
HEADING_STEPS = {"front": (0, 8, -8, 15), "overwing": (0, 8, -8), "wing": (0, 8, -8), "roar": (0, 8, -8)}
PITCH_STEPS = {"front": (0, -6), "overwing": (0,), "wing": (0,), "roar": (0,)}
SLOTS = {"1": ("front", "L"), "2": ("overwing", "L"), "3": ("wing", "L"), "4": ("roar", "L"),
         "5": ("front", "R"), "6": ("overwing", "R"), "7": ("wing", "R"), "8": ("roar", "R")}
# Alt+9 keeps the pilot view that was saved on each type before (old slot "3")
PILOT = {"319": ((-0.066833, 0.65112, -2.484581), (-9.703928, 0.052098, -0.55511), 0.371446),
         "320": ((-0.048139, 0.643688, -2.506579), (-8.516599, -0.011368, -0.110191), 0.370503),
         "321": ((-0.024983, 0.635429, -2.455647), (-9.00592, -0.001387, 0.161172), 0.394599)}
LAYOUTS = ["FNX_320_CFM_SL", "FNX_319_CFM_SL_HD", "FNX_319_CFM_SL_SD", "FNX_321_CFM_SL_SC", "FNX_321_CFM_SL_TC"]


def twins(rep):
    p = rep.split("_")
    return ["_".join(["FNX", p[1], e, w] + p[4:]) for e in ("CFM", "IAE") for w in ("SL", "WF")]


def run(rep, write):
    cache = os.path.join(OUT, rep, "views.json")
    if "--from-cache" in sys.argv:
        views = {k: tuple(v) for k, v in json.load(open(cache)).items()}
        print(f"{rep}: views from {cache}")
        write_files(rep, views, write)
        return
    t0 = time.time()
    typ = rep[4:7]
    eye = fx.eye_for(rep)
    win, glass_x = fx.windows(rep)
    cands = {}
    for s, (role, side) in SLOTS.items():
        target = ROLES[role][0]
        near = sorted(win[side], key=lambda z: abs(z - target))[:5 if role == "front" else 4]
        sign = -1 if side == "L" else 1
        cands[s] = [(sign * (glass_x - ins), CAM_Y, z) for z in near for ins in INSETS]
    # geometry around every candidate, plus the cockpit for slots 9/0
    pilot_xyz, pilot_pbh, pilot_zoom = PILOT[typ]
    pts = [p for c in cands.values() for p in c] + [(pilot_xyz[0] + eye[1], pilot_xyz[1] + eye[2], pilot_xyz[2] + eye[0])]
    pseudo = {str(i): vc.camera((p[0] - eye[1], p[1] - eye[2], p[2] - eye[0]), (0, 0), eye, ZOOM) for i, p in enumerate(pts)}
    gin, gext, gy = fx.scene(rep, pseudo, radius=3.6, verbose=False)

    def evaluate(xyz, pbh, zoom=ZOOM, w=32, h=18):
        cam = vc.camera(tuple(xyz), (math.radians(pbh[0]), math.radians(pbh[2])), eye, zoom)
        img, counts, core = vc.render(cam, gin, gext, gy, w, h)
        tot, ctot = sum(counts), sum(core)
        return (100 * (counts[7] + counts[8]) / tot, 100 * sum(core[k] for k in (0, 1, 2, 3)) / ctot,
                100 * (core[2] + core[3]) / ctot, 100 * core[3] / ctot, img[h // 2][w // 2], img)

    def score(role, r, dist, dh):
        bad, out, wing, eng, center = r[:5]
        if bad > 5 or center in (7, 8):
            return -1000 - bad
        if role == "front":   # the point of this view is the intake: seeing the engine beats seeing ground
            return 0.4 * out + 2.5 * eng + 0.3 * wing - 3 * bad - 12 * dist - 0.2 * abs(dh)
        return out + 0.5 * wing - 3 * bad - 12 * dist - 0.3 * abs(dh)

    rel = lambda p: [p[0] - eye[1], p[1] - eye[2], p[2] - eye[0]]
    views, notes = {}, []
    for s, (role, side) in SLOTS.items():
        target, pitch, hdg = ROLES[role]
        sign = -1 if side == "L" else 1
        ranked = sorted(((score(role, evaluate(rel(p), (pitch, 0, sign * hdg)), abs(p[2] - target), 0), p) for p in cands[s]), reverse=True)
        best = None
        for sc, p in ranked[:3]:
            for dh in HEADING_STEPS[role]:
                for dp in PITCH_STEPS[role]:
                    pbh = (pitch + dp, 0.0, sign * (hdg + dh))
                    sc2 = score(role, evaluate(rel(p), pbh), abs(p[2] - target), dh)
                    if best is None or sc2 > best[0]:
                        best = (sc2, p, pbh)
        sc, p, pbh = best
        bad, out, wing, eng, center, img = evaluate(rel(p), pbh, ZOOM, 96, 54)
        os.makedirs(os.path.join(OUT, rep), exist_ok=True)
        vc.write_png(os.path.join(OUT, rep, f"view_{s}.png"), img)
        views[s] = (rel(p), pbh, ZOOM)
        flag = "" if sc > -1000 else "  <-- NO GOOD SPOT"
        notes.append(f"  {s} {role:8s}{side}: z {p[2]:+.2f} (target {target:+.2f}), {glass_x - abs(p[0]):.2f} m in, hdg {pbh[2]:+.0f}: "
                     f"outside {out:.0f}% wing/engine {wing:.0f}% (engine {eng:.0f}%) bad {bad:.0f}% centre {vc.NAMES[center]}{flag}")
    # 9: pilot (kept), 0: GoPro just inside the captain-side windshield, 0.25 m left of centre
    views["9"] = (list(pilot_xyz), pilot_pbh, pilot_zoom)
    ws = mesh_points(fx.fuselage_model(rep), r"^Fuselage_Windshield_Window_L$")
    eye_y = eye[2] + pilot_xyz[1]
    wz = windshield_z(ws, eye_y)
    gz = (wz - 0.12) if wz else (eye[0] + pilot_xyz[2] + 0.30)
    views["0"] = ([-0.25 - eye[1], pilot_xyz[1], gz - eye[0]], (-7.6, 0.0, 0.0), 2.577039)
    for s in "90":
        bad, out, wing, eng, center, img = evaluate(views[s][0], views[s][1], views[s][2], 96, 54)
        vc.write_png(os.path.join(OUT, rep, f"view_{s}.png"), img)
        notes.append(f"  {s} {'pilot' if s == '9' else 'GoPro':9s}: outside {out:.0f}% bad {bad:.0f}% centre {vc.NAMES[center]}"
                     + (f" (windshield at z {wz:+.2f})" if s == "0" and wz else ""))
    print(f"{rep}  ({time.time() - t0:.0f}s)\n" + "\n".join(notes), flush=True)
    json.dump(views, open(cache, "w"), indent=1)
    write_files(rep, views, write)


def write_files(rep, views, write):
    for preset in twins(rep):
        dst = os.path.join(ROAM, preset, "config", "cameras.cfg")
        keep = ""
        if os.path.exists(dst):   # a camera titled "Pilot" (not an Alt slot) is carried over untouched
            m = re.search(r'\[CAMERADEFINITION\.\d+\]\s*\nTitle="Pilot".*?(?=\n\[CAMERADEFINITION|\Z)', open(dst, encoding="utf-8").read(), re.S)
            keep = re.sub(r"\[CAMERADEFINITION\.\d+\]", "[CAMERADEFINITION.10]", m.group(0).strip(), count=1) if m else ""
        out = ["[VERSION]", "major=1", "minor=0"]
        for idx, s in enumerate("0912345678"):
            xyz, pbh, zoom = views[s]
            out.append(block(idx, s, xyz, pbh, zoom))
        if keep:
            out.append(keep)
        if write:
            open(dst, "w", encoding="utf-8", newline="\r\n").write("\n".join(out) + "\n")
        print(f"    {'wrote' if write else 'would write'} {preset}" + (" (kept its 'Pilot' camera)" if keep else ""))


if __name__ == "__main__":
    only = sys.argv[sys.argv.index("--only") + 1].split(",") if "--only" in sys.argv else LAYOUTS
    for rep in only:
        run(rep, "--write" in sys.argv)
