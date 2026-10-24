"""Shared view search for the sound-tuned camera layout (used for the iFly and FlyByWire; genfnx.py has its own copy).

Layout: 1/5 engine front, 2/6 over-wing (slats), 3/7 wing (flaps, hydraulics), 4/8 behind the wing (roar);
1-4 left, 5-8 right; 9 = the aircraft's existing pilot view, 0 = windshield GoPro.

An aircraft adapter is a dict:
  eye (lon, lat, vert m), windows {"L": [z], "R": [z]}, wall_x (|x| of the reference window plane),
  insets, cam_y (absolute head height), roles {role: (target z, pitch, heading)}, scene(pseudo_cams),
  pilot (xyz, pbh, zoom), windshield_pts (glTF points of the captain-side windshield), png_dir.
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import viewcheck as vc  # noqa: E402
from gen737 import windshield_z, block  # noqa: E402

ZOOM = 0.354
SLOTS = {"1": ("front", "L"), "2": ("overwing", "L"), "3": ("wing", "L"), "4": ("roar", "L"),
         "5": ("front", "R"), "6": ("overwing", "R"), "7": ("wing", "R"), "8": ("roar", "R")}
HEADING_STEPS = {"front": (0, 8, -8, 15), "overwing": (0, 8, -8), "wing": (0, 8, -8), "roar": (0, 8, -8)}
PITCH_STEPS = {"front": (0, -6), "overwing": (0,), "wing": (0,), "roar": (0,)}


def search(ac):
    eye = ac["eye"]
    rel = lambda p: [p[0] - eye[1], p[1] - eye[2], p[2] - eye[0]]
    cands = {}
    for s, (role, side) in SLOTS.items():
        target = ac["roles"][role][0]
        near = sorted(ac["windows"][side], key=lambda z: abs(z - target))[:5 if role == "front" else 4]
        sign = -1 if side == "L" else 1
        cands[s] = [(sign * (ac["wall_x"] - ins), ac["cam_y"], z) for z in near for ins in ac["insets"]]
    pilot_xyz, pilot_pbh, pilot_zoom = ac["pilot"]
    pts = [p for c in cands.values() for p in c] + [(pilot_xyz[0] + eye[1], pilot_xyz[1] + eye[2], pilot_xyz[2] + eye[0])]
    pseudo = {str(i): vc.camera(tuple(rel(p)), (0, 0), eye, ZOOM) for i, p in enumerate(pts)}
    gin, gext, gy = ac["scene"](pseudo)

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
        if role == "front":
            return 0.4 * out + 2.5 * eng + 0.3 * wing - 3 * bad - 12 * dist - 0.2 * abs(dh)
        return out + 0.5 * wing - 3 * bad - 12 * dist - 0.3 * abs(dh)

    views, notes = {}, []
    os.makedirs(ac["png_dir"], exist_ok=True)
    for s, (role, side) in SLOTS.items():
        target, pitch, hdg = ac["roles"][role]
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
        vc.write_png(os.path.join(ac["png_dir"], f"view_{s}.png"), img)
        views[s] = (rel(p), pbh, ZOOM)
        notes.append(f"  {s} {role:8s}{side}: z {p[2]:+.2f} (target {target:+.2f}), {ac['wall_x'] - abs(p[0]):.2f} m in, hdg {pbh[2]:+.0f}: "
                     f"outside {out:.0f}% wing/engine {wing:.0f}% (engine {eng:.0f}%) bad {bad:.0f}% centre {vc.NAMES[center]}"
                     + ("" if sc > -1000 else "  <-- NO GOOD SPOT"))
    views["9"] = (list(pilot_xyz), pilot_pbh, pilot_zoom)
    eye_y = eye[2] + pilot_xyz[1]
    wz = windshield_z(ac["windshield_pts"], eye_y) if ac.get("windshield_pts") else None
    gz = (wz - 0.12) if wz else (eye[0] + pilot_xyz[2] + 0.30)
    views["0"] = ([-0.25 - eye[1], pilot_xyz[1], gz - eye[0]], (-7.6, 0.0, 0.0), 2.577039)
    for s in "90":
        bad, out, wing, eng, center, img = evaluate(views[s][0], views[s][1], views[s][2], 96, 54)
        vc.write_png(os.path.join(ac["png_dir"], f"view_{s}.png"), img)
        notes.append(f"  {s} {'pilot' if s == '9' else 'GoPro':9s}: outside {out:.0f}% bad {bad:.0f}% centre {vc.NAMES[center]}"
                     + (f" (windshield at z {wz:+.2f})" if s == "0" and wz else " (windshield estimated)" if s == "0" else ""))
    return views, notes


def camera_file(views, extra_blocks=()):
    out = ["[VERSION]", "major=1", "minor=0"]
    for idx, s in enumerate("0912345678"):
        xyz, pbh, zoom = views[s]
        out.append(block(idx, s, xyz, pbh, zoom))
    out.extend(extra_blocks)
    return "\n".join(out) + "\n"
