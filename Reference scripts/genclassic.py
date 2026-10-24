"""Sound-tuned views for the single-model aircraft: iFly 737 MAX 8 (4 cabin variants) and FlyByWire A32NX.

Usage: genclassic.py ifly|fbw [--only <variant>] [--write] [--from-cache]
Same layout and search as the Fenix (genviews.search). Old view files are replaced only with --write.
"""
import json, os, re, sys, time
sys.path.insert(0, os.path.dirname(__file__))
import viewcheck as vc  # noqa: E402
import genviews as gv  # noqa: E402
from gen737 import mesh_points, window_centers  # noqa: E402

C = r"D:\MSFS2024 Community\Community"
ROAM = os.path.expandvars(r"%APPDATA%\Microsoft Flight Simulator 2024\SimObjects\Airplanes")
OUT = os.path.join(os.path.dirname(__file__), "vc")
FT = vc.FT
# Fuselage_MASK_*: the iFly interior's fuselage skin cuts its window holes with an alpha mask (texture), which a
# ray-caster can't see; the side-wall panels inside it have real openings and still bound the view
BASE_SKIP = r"collision|occluder|drone|glass|window_?pane|Cover|SafetyCone|Chock|^attachpt|Mouse|Animation_CabinWindow|^SOUND_|^Fuselage_MASK"
SKIP_MATS = r"glass|windshield|wind_?shield|windowsUV|windowsICE|invisible|collision|^TM_|_TM$"

_orig_mat_class = vc.mat_class


def mat_class(g, mi):
    if mi is not None:
        m = g["materials"][mi]
        if re.search(SKIP_MATS, m.get("name", ""), re.I):
            return "skip", False
        # iFly interior fuselage skins (Fuselage_1, Fuselage_MASK_03, ...) cut their windows with an alpha mask
        if m.get("alphaMode") == "MASK" and re.match(r"Max8(200)?_Fuselage\d", m.get("name", "")):
            return "skip", False
    return _orig_mat_class(g, mi)


vc.mat_class = mat_class


def model_file(xml):
    text = open(xml, encoding="utf-8", errors="replace").read()
    m = re.search(r'ModelFile="([^"]+)"', text)
    return os.path.normpath(os.path.join(os.path.dirname(xml), m.group(1)))


def classic_scene(int_files, ext_files, engine_pat, radius=3.6, lining_pat=None):
    """lining_pat: exterior meshes that face into the cabin (FBW HublotIn window lining). They go in the culled
    exterior grid but as class 4, so seen from inside they block like a wall and from behind they vanish, as in the sim."""
    def scene(pseudo):
        spheres = [(*c[0], radius) for c in pseudo.values()]
        tris, etris = [], []
        for f in int_files:
            vc.load_tris(f, None, 4, spheres, tris, BASE_SKIP)
        big = [(*spheres[0][:3], 80.0)]
        for f in ext_files:
            vc.load_tris(f, None, 3, big, etris, BASE_SKIP + "|^(?!.*(?:" + engine_pat + "))")
            if lining_pat:
                vc.load_tris(f, None, 4, big, etris, BASE_SKIP + "|^(?!.*(?:" + lining_pat + "))")
            vc.load_tris(f, None, 2, big, etris, BASE_SKIP + "|" + engine_pat + ("|" + lining_pat if lining_pat else ""))
        ground_y = min(t[5][1] for t in etris)
        print(f"  loaded {len(tris)} interior / {len(etris)} exterior tris", flush=True)
        return vc.Grid(tris, 0.12), vc.Grid(etris, 1.0), ground_y
    return scene


# ------------------------------------------------------------------ iFly 737 MAX 8
IFLY = os.path.join(C, r"ifly-aircraft-737max8\SimObjects\Airplanes")
IFLY_VARIANTS = {"iFly 737-MAX8": "178Seat", "iFly 737-MAX8-166Seats": "166Seat", "iFly 737-MAX8-189Seats": "189Seat", "iFly 737-MAX8200": "8200"}
IFLY_PILOT = ((0.005823, 0.013122, -0.37368), (-14.033906, -0.166283, 0.079032), 0.337902)   # the pack's own pilot view (old Alt+0)
IFLY_ENGINE = r"ENG\d|Engine_\d|ENG_ICE"


def ifly(variant):
    cfg = open(os.path.join(IFLY, variant, f"model.{IFLY_VARIANTS[variant]}", "model.CFG"), encoding="utf-8").read()
    folder = os.path.join(IFLY, variant, f"model.{IFLY_VARIANTS[variant]}")
    ext = model_file(os.path.normpath(os.path.join(folder, re.search(r"normal\s*=\s*(\S.*)", cfg).group(1).strip())))
    intr = model_file(os.path.normpath(os.path.join(folder, re.search(r"interior\s*=\s*(\S.*)", cfg).group(1).strip())))
    # window positions along the cabin: the Animation_CabinWindow_* shades (they slide up/down, so their z is
    # the window's); height and glass depth: the interior's separate glass meshes (only the exits have them)
    import statistics
    eye = (49.683998 * FT, -1.63 * FT, 2.1 * FT)
    win = {s: window_centers(mesh_points(ext, r"^Animation_CabinWindow_[LR]_\d+$"), s) for s in "LR"}
    glass_pat = r"^Fuselage_Windows(UV_Obj|Glass)"
    pts = [p for p in mesh_points(intr, glass_pat) if abs(p[0]) > 1.5 and p[2] < 12.5]
    names = [n.get("name", "") for n in json.load(open(intr, encoding="utf-8"))["nodes"] if "mesh" in n and re.match(glass_pat, n.get("name", ""))]
    centres = []
    for nm in names:
        ys_n = [p[1] for p in mesh_points(intr, "^" + re.escape(nm) + "$") if abs(p[0]) > 1.5]
        if ys_n:
            centres.append((min(ys_n) + max(ys_n)) / 2)
    win_y = statistics.median(centres)
    # safety cones in front of the engines and the red covers are ground props, not the nacelle
    inlet = max(p[2] for p in mesh_points(ext, r"^(?!.*(?:Cover|SafetyCone)).*(?:" + IFLY_ENGINE + ")"))
    print(f"{variant}: exterior {os.path.basename(ext)}, interior {os.path.basename(intr)}; {len(win['L'])}/{len(win['R'])} windows, "
          f"glass |x| {statistics.median(abs(p[0]) for p in pts):.3f}, median window centre y {win_y:.3f}, engine front z {inlet:+.2f}")
    return {"eye": eye, "windows": win, "wall_x": statistics.median(abs(p[0]) for p in pts), "insets": (0.22, 0.28, 0.35, 0.42),
            "cam_y": win_y + 0.03,
            "roles": {"front": (inlet + 1.5, -25.0, 115.0), "overwing": (0.0, -14.0, 92.0), "wing": (-3.1, -13.0, 75.0), "roar": (-6.2, -12.0, 68.0)},
            "scene": classic_scene([intr], [ext], IFLY_ENGINE), "pilot": IFLY_PILOT,
            "windshield_pts": [p for p in mesh_points(ext, r"^VC_MC_Window_Glass_F_\d+$") if p[0] > 0],
            "png_dir": os.path.join(OUT, "ifly_new", variant.replace(" ", "_")), "dst": os.path.join(ROAM, variant, "cameras.CFG")}


# ------------------------------------------------------------------ FlyByWire A32NX
FBW = os.path.join(C, r"flybywire-aircraft-a320-neo\SimObjects\AirPlanes\FlyByWire_A320_NEO\model")
FBW_PILOT = ((-0.044968, 0.769978, -2.274009), (-12.164747, -0.000579, 0.347807), 0.352379)   # the previous FlyByWire pilot view
FBW_ENGINE = r"REACTOR|PROP_"


def fbw(_variant):
    import fnxcheck as fx   # the A32NX shares the A320 fuselage: windows from the Fenix A320, whose datum matches
    ext, intr = os.path.join(FBW, "A320_NEO_LOD00.gltf"), os.path.join(FBW, "A320_NEO_INTERIOR_LOD00.gltf")
    win, _ = fx.windows("FNX_320_CFM_SL")
    ws_f = mesh_points(fx.fuselage_model("FNX_320_CFM_SL"), r"^Fuselage_Windshield_Window_L$")
    ws_b = [p for p in mesh_points(ext, r"^WINDSHIELD$") if p[0] > 0]
    dy = min(p[1] for p in ws_b if p[0] < 0.9) - min(p[1] for p in ws_f)
    dz = max(p[2] for p in ws_b if p[0] < 0.9) - max(p[2] for p in ws_f)
    inlet = max(p[2] for p in mesh_points(ext, r"^REACTOR_LEFT$"))
    print(f"FlyByWire: windshield vs Fenix: dy {dy:+.3f} m, dz {dz:+.3f} m; LEAP inlet z {inlet:+.2f}; windows from the Fenix A320 (+dz)")
    win = {s: [z + dz for z in v] for s, v in win.items()}
    # HublotIn: window lining just inside the hull (|x| 1.70-1.92 at seat height, z -8.4..+1.2) that faces the cabin;
    # cameras have to sit in the gap between it and the hull (|x| 1.80-1.96) to see out
    return {"eye": (43.72074 * FT, -1.723061 * FT, 4.355627 * FT), "windows": win, "wall_x": 1.95, "insets": (0.04, 0.06, 0.08, 0.11, 0.14),
            # windows are painted on, and windshield/pilot-eye offsets disagree (+0.56 / +0.25 m): use the height
            # of the four previous FlyByWire window views (y 0.73 above the eyepoint = 2.058 m)
            "cam_y": 4.355627 * FT + 0.73,
            "roles": {"front": (inlet + 1.4, -25.0, 115.0), "overwing": (-0.57 + dz, -14.0, 92.0), "wing": (-4.6 + dz, -13.0, 75.0), "roar": (-7.8 + dz, -12.0, 68.0)},
            "scene": classic_scene([intr], [ext], FBW_ENGINE, lining_pat=r"^HublotIn"), "pilot": FBW_PILOT, "windshield_pts": ws_b,
            "png_dir": os.path.join(OUT, "fbw_new"), "dst": os.path.join(ROAM, "FlyByWire_A320_NEO", "cameras.CFG")}


if __name__ == "__main__":
    kind = sys.argv[1]
    variants = list(IFLY_VARIANTS) if kind == "ifly" else ["FlyByWire_A320_NEO"]
    if "--only" in sys.argv:
        variants = [sys.argv[sys.argv.index("--only") + 1]]
    for v in variants:
        ac = ifly(v) if kind == "ifly" else fbw(v)
        cache = os.path.join(ac["png_dir"], "views.json")
        if "--from-cache" in sys.argv:
            views = {k: tuple(x) for k, x in json.load(open(cache)).items()}
        else:
            t0 = time.time()
            views, notes = gv.search(ac)
            json.dump(views, open(cache, "w"), indent=1)
            print(f"{v}  ({time.time() - t0:.0f}s)\n" + "\n".join(notes), flush=True)
        if "--write" in sys.argv:
            open(ac["dst"], "w", encoding="utf-8", newline="\r\n").write(gv.camera_file(views))
        print(f"    {'wrote' if '--write' in sys.argv else 'would write'} {ac['dst']}")
