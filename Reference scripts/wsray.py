"""Find the front windshield at the GoPro spot by ray casting with glass treated as solid.

From 0.25 m left of centre at pilot-eye height, cast straight ahead (and a few degrees up/down) from the
pilot's eye and print the first surfaces hit. Usage: wsray.py fenix <preset> | wsray.py fbw
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import viewcheck as vc  # noqa: E402

FT = 0.3048
_orig = vc.mat_class
vc.mat_class = lambda g, mi: ("opaque", True) if mi is not None and "invisible" not in " ".join(g["materials"][mi].get("extensions", {})).lower() else _orig(g, mi)
KEEP = r"collision|occluder|^Skel_|Mouse|^attachpt"

if sys.argv[1] == "fenix":
    import fnxcheck as fx
    preset = sys.argv[2]
    eye = fx.eye_for(preset)
    pilot_y = {"319": 0.65112, "320": 0.643688, "321": 0.635429}[preset[4:7]]
    pilot_z = {"319": -2.484581, "320": -2.506579, "321": -2.455647}[preset[4:7]]
    start = (0.25, eye[2] + pilot_y, eye[0] + pilot_z)
    tris = []
    for kind in ("interior", "exterior"):
        for L, A, name in fx.place(fx.assemble(preset, kind)):
            for f in L[0]:
                vc.load_tris(f, A, 4, [(*start, 2.5)], tris, KEEP)
else:
    m = r"D:\MSFS2024 Community\Community\flybywire-aircraft-a320-neo\SimObjects\AirPlanes\FlyByWire_A320_NEO\model"
    eye = (43.72074 * FT, -1.723061 * FT, 4.355627 * FT)
    pilot_y, pilot_z = 0.769978, -2.274009
    start = (0.25, eye[2] + pilot_y, eye[0] + pilot_z)
    tris = []
    for f in ("A320_NEO_LOD00.gltf", "A320_NEO_INTERIOR_LOD00.gltf"):
        vc.load_tris(os.path.join(m, f), None, 4, [(*start, 2.5)], tris, KEEP)
g = vc.Grid(tris, 0.12)
print(f"start (glTF) x {start[0]:+.2f} y {start[1]:.3f} z {start[2]:+.3f}; {len(tris)} tris")
for el in (6, 3, 0, -3, -6):
    e = math.radians(el)
    d = (0.0, math.sin(e), math.cos(e))
    # walk along the ray, reporting up to 3 successive surfaces
    o, out, travelled = start, [], 0.0
    for _ in range(3):
        h = g.cast(o, d, 3.0 - travelled)
        if not h:
            break
        t = h[0]
        p = tuple(o[k] + d[k] * t for k in range(3))
        out.append(f"{travelled + t:.2f} m (z {p[2]:+.2f}) {tris[h[1]][7][:70]}")
        o = tuple(p[k] + d[k] * 0.002 for k in range(3))
        travelled += t + 0.002
    print(f"  pitch {el:+d}: " + ("  ->  ".join(out) if out else "nothing within 3 m"))
