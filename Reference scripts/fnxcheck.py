"""Offline view check for the Fenix A319/A320/A321 (MSFS 2024 modular, split over two packages).

Differences from the PMDG checkrun: attachment roots and model files resolve across both Fenix
packages (as the sim's VFS does); model XMLs may use <LODS Template=...> and per-LOD <MergeModel>;
and every part - interior and exterior - is placed at its attach_to_node, whose world matrix comes
from the parts loaded before it.

Usage: fnxcheck.py <preset> <cameras.cfg> <out dir> [--slots 1,2] [--windows]
"""
import os, re, sys, time
sys.path.insert(0, os.path.dirname(__file__))
import viewcheck as vc  # noqa: E402
from nodes import mat_mul  # noqa: E402
from gen737 import mesh_points, window_centers  # noqa: E402

C = r"D:\MSFS2024 Community\Community"
PKGS = [os.path.join(C, "fnx-aircraft-320"), os.path.join(C, "fnx-aircraft-319-321")]
AC = r"SimObjects\Airplanes\FNX_32X"
FT = vc.FT
EYE_FT = {"319": 38.650528, "320": 43.920738, "321": 57.965850}   # lon; lat -1.623061, vert 3.955627 ft
EYE_LAT_FT, EYE_VERT_FT = -1.623061, 3.955627
# viewcheck's default skip list has "pane", which would drop every Fenix "Wall_Panel"; Skel_* are
# huge helper boxes/planes of the Fenix cabin rig, not rendered geometry
SKIP = r"collision|occluder|drone|glass|window_?pane|^Skel_"


def eye_for(preset):
    return (EYE_FT[preset[4:7]] * FT, EYE_LAT_FT * FT, EYE_VERT_FT * FT)


def resolve(rel):
    for p in PKGS:
        f = os.path.normpath(os.path.join(p, rel.replace("/", "\\")))
        if os.path.exists(f):
            return f
    return None


def rel_of(path):
    for p in PKGS:
        if path.lower().startswith(p.lower() + "\\"):
            return path[len(p) + 1:]
    raise ValueError(path)


def lods(xml):
    """LOD list; each entry is [model, *merged models]. Follows <LODS Template=...> and <MergeModel>."""
    base = os.path.dirname(rel_of(xml))
    text = open(xml, encoding="utf-8", errors="replace").read()
    res = lambda m: resolve(os.path.normpath(os.path.join(base, m.strip())))
    out = []
    t = re.search(r'<LODS\b[^>]*\bTemplate="([^"]+)"', text)
    if t and res(t.group(1)):
        out = [list(e) for e in lods(res(t.group(1)))]
    for f in re.findall(r'<LOD\b[^>]*\bModelFile="([^"]+)"', text):
        if res(f):
            out.append([res(f)])
    for idx, body in re.findall(r'<LOD\b[^>]*\bIndex="(\d+)"[^>]*>(.*?)</LOD>', text, re.S):
        for m in re.findall(r"<MergeModel>([^<]+)</MergeModel>", body):
            if res(m) and int(idx) < len(out):
                out[int(idx)].append(res(m))
    return out


def assemble(preset, kind):
    """Depth-first, parents before children: [(lods, attach node, part folder, offset)]."""
    parts, seen = [], set()

    def visit(cfg_rel, inherited):
        cfg = resolve(cfg_rel)
        if not cfg or cfg.lower() in seen:
            return
        seen.add(cfg.lower())
        for s in vc.cfg_sections(cfg):
            if not s["__name"].startswith("SIM_ATTACHMENT"):
                continue
            k = s.get("attach_to_model", inherited)
            root = s.get("attachment_root", "").replace("/", "\\")
            if k == kind and "attachment_file" in s:
                xml = resolve(os.path.join(root, s["attachment_file"]))
                L = lods(xml) if xml else []
                if L:
                    off = tuple(float(v) for v in s["attach_offset"].split(",")) if "attach_offset" in s else None
                    parts.append((L, s.get("attach_to_node"), os.path.basename(root), off))
                elif xml is None:
                    print(f"  ! missing {root}\\{s['attachment_file']}")
            visit(os.path.join(root, "config", "attached_objects.cfg"), k)
    visit(os.path.join(AC, "presets", "fnx", preset, "config", "attached_objects.cfg"), kind)
    return parts


def place(parts, verbose=False):
    """World matrix per part from its attach node (searched in parts placed earlier)."""
    mats, placed = {}, []
    for L, node, name, off in parts:
        A = vc.attach_matrix(mats, node, off)
        if node and node not in mats and verbose:
            print(f"  ! attach node {node} not found for {name}")
        for f in L[0]:
            g, nodes, world = vc.load_gltf(f)
            for i, n in enumerate(nodes):
                mats.setdefault(n.get("name", ""), mat_mul(A, world(i)) if A else world(i))
        placed.append((L, A, name))
    return placed


def scene(preset, cams, radius=4.5, verbose=True):
    t0 = time.time()
    spheres = [(*c[0], radius) for c in cams.values()]
    tris = []
    for L, A, name in place(assemble(preset, "interior")):
        cls = 6 if "Cockpit" in name else 5 if "Seats" in name else 4
        # seats only need to occlude: their LOD3 keeps the shape at a fraction of the memory (LOD1 runs took 7 GB)
        n = sum(vc.load_tris(f, A, cls, spheres, tris, SKIP) for f in L[min(3 if cls == 5 else 0, len(L) - 1)])
        if n and verbose:
            print(f"  interior {name:44s} +{n}")
    etris = []
    big = [(*spheres[0][:3], 80.0)]
    for L, A, name in place(assemble(preset, "exterior")):
        cls = 3 if re.match(r"Part_Exterior_(CFM|IAE)", name) else 2   # not Function_Exterior_A320_CFM_SL (the fuselage)
        for f in L[min(2, len(L) - 1)]:
            vc.load_tris(f, A, cls, big, etris, SKIP)
    ground_y = min((t[5][1] for t in etris), default=-5.0)
    if verbose:
        print(f"loaded {len(tris)} interior / {len(etris)} exterior tris in {time.time() - t0:.0f}s, ground y {ground_y:.2f}")
    return vc.Grid(tris, 0.12), vc.Grid(etris, 1.0), ground_y


def fuselage_model(preset):
    for L, node, name, off in assemble(preset, "exterior"):
        if "\\Part_Exterior_Fuselage_A3" in L[0][0]:
            return L[0][0]


def windows(preset):
    pts = mesh_points(fuselage_model(preset), r"^Fuselage_Glass_Cabin$")
    return {s: window_centers(pts, s) for s in "LR"}, (sum(abs(p[0]) for p in pts) / len(pts) if pts else None)


def report(cams, gin, gext, ground_y, outdir):
    os.makedirs(outdir, exist_ok=True)
    for name, cam in sorted(cams.items()):
        img, counts, core = vc.render(cam, gin, gext, ground_y)
        vc.write_png(os.path.join(outdir, f"view_{name}.png"), img)
        tot, ctot = sum(counts), sum(core)
        pct = lambda arr, ks, T: round(100 * sum(arr[k] for k in ks) / T)
        print(f"view {name:>6}: outside {pct(core, (0, 1, 2, 3), ctot):3d}%  wing/engine {pct(core, (2, 3), ctot):3d}% (whole frame {pct(counts, (2, 3), tot):3d}%)  "
              f"interior {pct(core, (4, 5, 6), ctot):3d}%  bad {pct(counts, (7, 8), tot):3d}%  enclosure {round(100 * vc.enclosure(cam, gin)):3d}%  "
              f"center {vc.NAMES[img[len(img) // 2][len(img[0]) // 2]]}")


if __name__ == "__main__":
    preset, camfile, outdir = sys.argv[1:4]
    eye = eye_for(preset)
    if "--windows" in sys.argv:
        w, lat = windows(preset)
        print(f"glass |x| {lat:.3f} m; L windows (datum z): " + " ".join(f"{z:+.2f}" for z in w["L"]))
        print("R windows: " + " ".join(f"{z:+.2f}" for z in w["R"]))
    cams = vc.read_cameras(camfile, eye)
    if "--slots" in sys.argv:
        keep = sys.argv[sys.argv.index("--slots") + 1].split(",")
        cams = {k: v for k, v in cams.items() if k in keep}
    gin, gext, gy = scene(preset, cams)
    report(cams, gin, gext, gy, outdir)
