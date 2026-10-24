"""Generate sound-tuned custom camera files for every PMDG 737 preset.

Slots (same roles as the 777 set):
  1/5 engine front, 2/6 over-wing (flap motor at the datum), 3/7 wing + hydraulic pumps (L_EHP/R_EHP),
  4/8 exhaust roar, 9 pilot seat, 0 windshield GoPro.  1-4 left side, 5-8 right side.
Usage: gen737.py [--write]
"""
import json, os, re, struct, sys, uuid
sys.path.insert(0, os.path.dirname(__file__))
from nodes import local_matrix, mat_mul  # noqa: E402

COMMUNITY = r"D:\MSFS2024 Community\Community"
ROAMING = os.path.expandvars(r"%APPDATA%\Microsoft Flight Simulator 2024\SimObjects\Airplanes")
FT = 0.3048
FAMILIES = {
    "737-700": ("pmdg-aircraft-737", 37.31212336),
    "737-800": ("pmdg-aircraft-738", 47.07464336),
    "737-900": ("pmdg-aircraft-739", 52.13864336),
}
EYE_LAT, EYE_VERT = -1.660 * FT, 3.909 * FT
PILOT_XYZ, PILOT_PBH, ZOOM = (0.00115, 0.363966, -0.520507), (-11.377, 0.0, 0.0), 0.354
CAM_LAT, CAM_Y = 1.55, 1.375          # window-seat head position (datum frame, m)
WINDOW_PAT = r"^(cabin_window_glass\d*|pax_window_glass|900ER_pax_window_glass)$"
# role: (target datum z in m, pitch, heading magnitude); heading sign: left negative, right positive
ROLES = {
    "front": (6.0, -20.0, 120.0),
    "overwing": (0.0, -14.0, 92.0),
    "wing_hyd": (-3.144, -13.0, 62.0),
    "roar": (-6.2, -12.0, 65.0),
}
SLOTS = {"1": ("front", "L"), "2": ("overwing", "L"), "3": ("wing_hyd", "L"), "4": ("roar", "L"),
         "5": ("front", "R"), "6": ("overwing", "R"), "7": ("wing_hyd", "R"), "8": ("roar", "R")}


def fuselage_for(fam, preset):
    if fam == "737-700":
        return ("737BBJ_Fuselage", "BBJ_Fuselage") if "BBJ" in preset else ("737BDSF_Fuselage", "BDSF_Fuselage") if "BDSF" in preset else ("737_Fuselage", "737_Fuselage")
    if fam == "737-800":
        for key, fn in (("BBJ2", "BBJ2_Fuselage"), ("BCF", "BCF_Fuselage"), ("BDSF", "BDSF_Fuselage")):
            if key in preset:
                return ("738" + key + "_Fuselage", fn)
        return ("738_Fuselage", "738_Fuselage")
    return ("739ER_Fuselage", "739ER_Fuselage") if "900ER" in preset else ("739_Fuselage", "739_Fuselage")


def mesh_points(path, pat):
    g = json.load(open(path, encoding="utf-8"))
    nodes = g["nodes"]
    parent = {c: i for i, n in enumerate(nodes) for c in n.get("children", [])}

    def world(i):
        m = local_matrix(nodes[i])
        while i in parent:
            i = parent[i]
            m = mat_mul(local_matrix(nodes[i]), m)
        return m
    pts, f = [], None
    for i, n in enumerate(nodes):
        if "mesh" not in n or not re.search(pat, n.get("name", ""), re.I):
            continue
        w = world(i)
        for p in g["meshes"][n["mesh"]]["primitives"]:
            acc = g["accessors"][p["attributes"]["POSITION"]]
            bv = g["bufferViews"][acc["bufferView"]]
            if f is None:
                f = open(os.path.join(os.path.dirname(path), g["buffers"][bv["buffer"]]["uri"]), "rb")
            stride = bv.get("byteStride", 12)
            f.seek(bv.get("byteOffset", 0) + acc.get("byteOffset", 0))
            raw = f.read(stride * (acc["count"] - 1) + 12)
            for k in range(acc["count"]):
                x, y, z = struct.unpack_from("<3f", raw, k * stride)
                pts.append(tuple(sum(w[r][c] * v for c, v in enumerate((x, y, z))) + w[r][3] for r in range(3)))
    return pts


def window_centers(pts, side):
    sel = [p for p in pts if (p[0] > 0.5 if side == "L" else p[0] < -0.5)]
    sel.sort(key=lambda p: p[2])
    groups, cur = [], []
    for p in sel:
        if cur and p[2] - cur[-1][2] > 0.12:
            groups.append(cur)
            cur = []
        cur.append(p)
    if cur:
        groups.append(cur)
    return [(min(q[2] for q in g) + max(q[2] for q in g)) / 2 for g in groups]


def windshield_z(pts, y_target, x_target=0.25):
    """Datum z of the captain-side front windshield glass at a given height and lateral offset.

    The pane is defined only by its corners, so interpolate z along the inboard edge (next to the
    center post) and the outboard edge at the target height, then across to x_target.
    """
    def edge_z(edge):
        lo, hi = min(edge, key=lambda p: p[1]), max(edge, key=lambda p: p[1])
        if hi[1] - lo[1] < 0.05:
            return None
        return lo[2] + (y_target - lo[1]) / (hi[1] - lo[1]) * (hi[2] - lo[2]), (lo[0] + hi[0]) / 2

    inner = edge_z([p for p in pts if 0.0 < p[0] < 0.2]) if any(0.0 < p[0] < 0.2 for p in pts) else None
    outer = edge_z([p for p in pts if 0.6 < p[0] < 0.9]) if any(0.6 < p[0] < 0.9 for p in pts) else None
    if not inner or not outer:
        return None
    (zi, xi), (zo, xo) = inner, outer
    return zi + (x_target - xi) / (xo - xi) * (zo - zi)


def block(idx, title, xyz, pbh, zoom):
    return "\n".join([
        f"[CAMERADEFINITION.{idx}]", f'Title="{title}"', f'Guid="{{{str(uuid.uuid4()).upper()}}}"', f'UITitle="{title}"',
        'Description=""', 'Origin="Virtual Cockpit"', 'Track="None"', 'TargetCategory="None"', 'ClipMode="Normal"',
        'SnapPbhAdjust="None"', 'PanPbhAdjust="None"', "XyzAdjust=0", 'ShowAxis="NO"', "AllowZoom=1",
        f"InitialZoom={zoom}", "SmoothZoomTime=5", "BoundingBoxRadius=0.1", "ShowWeather=0", "CycleHidden=0",
        "CycleHideRadius=0", "ShowPanel=0", "MomentumEffect=0", "ShowLensFlare=0", "PanPbhReturn=0", "SnapPbhReturn=1",
        "InstancedBased=0", "NoSortTitle=0", "Transition=0", 'Category="Cockpit"', 'SubCategory="Custom"',
        'SubCategoryItem="None"', "InitialXyz= {:.6f}, {:.6f}, {:.6f}".format(*xyz), "InitialPbh= {:.6f}, {:.6f}, {:.6f}".format(*pbh)])


def main():
    write = "--write" in sys.argv
    cache = {}
    for fam, (pkg, eye_ft) in FAMILIES.items():
        eye_lon = eye_ft * FT
        base = os.path.join(COMMUNITY, pkg, "SimObjects", "Airplanes", "PMDG " + fam)
        for preset in sorted(os.listdir(os.path.join(base, "presets", "pmdg"))):
            folder, fn = fuselage_for(fam, preset)
            model = os.path.join(base, "attachments", "pmdg", "Part_Exterior_" + folder, "model", fn + "_LOD0.gltf")
            if model not in cache:
                wpts = mesh_points(model, WINDOW_PAT)
                cpts = mesh_points(model, r"^cockpit_windows$")
                cache[model] = ({s: window_centers(wpts, s) for s in "LR"}, cpts)
            wins, cpts = cache[model]
            out, notes = ["[VERSION]", "major=1", "minor=0"], []
            for idx, slot in enumerate("0912345678"):
                if slot == "9":
                    out.append(block(idx, slot, PILOT_XYZ, PILOT_PBH, ZOOM))
                    continue
                if slot == "0":
                    eye_y = EYE_VERT + PILOT_XYZ[1]
                    wz = windshield_z(cpts, eye_y)
                    gz = (wz - 0.12) if wz else (eye_lon + PILOT_XYZ[2] + 0.30)
                    xyz = (-0.25 - EYE_LAT, PILOT_XYZ[1], gz - eye_lon)
                    out.append(block(idx, slot, xyz, (-7.6, 0.0, 0.0), 2.577039))
                    notes.append(f"0:gopro z={gz:.2f}" + ("" if wz else "(est)"))
                    continue
                role, side = SLOTS[slot]
                target, pitch, hdg = ROLES[role]
                cands = wins[side]
                z = min(cands, key=lambda w: abs(w - target)) if cands else target
                sign = -1 if side == "L" else 1
                xyz = (sign * CAM_LAT - EYE_LAT, CAM_Y - EYE_VERT, z - eye_lon)
                out.append(block(idx, slot, xyz, (pitch, 0.0, sign * hdg), ZOOM))
                notes.append(f"{slot}:{role}{side} z={z:.2f}" + ("" if cands else "(no window)"))
            dst = os.path.join(ROAMING, "PMDG " + fam, "presets", "pmdg", preset, "config", "cameras.CFG")
            print(f"{fam} | {preset:24s} | {fn:16s} | " + "  ".join(notes))
            if write:
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                open(dst, "w", encoding="utf-8", newline="\r\n").write("\n".join(out) + "\n")
    print("written" if write else "dry run (add --write)")


if __name__ == "__main__":
    main()
