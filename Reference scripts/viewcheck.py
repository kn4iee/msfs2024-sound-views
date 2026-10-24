"""Offline check of MSFS custom camera views against PMDG model geometry.

For each saved camera (cameras.CFG) it ray-casts the preset's real cabin/cockpit/seat models
(assembled from the attached_objects.cfg chain) and the exterior models, then reports what the
view shows and renders a small PNG.

Classes: 0 sky, 1 ground, 2 airframe (wing/fuselage), 3 engine, 4 cabin, 5 seat, 6 cockpit,
         7 backface (camera inside/behind a surface), 8 too close (near-clip).
"""
import json, math, os, re, struct, sys, zlib
sys.path.insert(0, os.path.dirname(__file__))
from nodes import local_matrix, mat_mul  # noqa: E402

FT = 0.3048
NEAR = 0.07
R_INT = 3.5

# ---------------------------------------------------------------- config / attachments

def cfg_sections(path):
    secs, cur = [], None
    for line in open(path, encoding="utf-8", errors="replace"):
        line = line.split(";")[0].split("//")[0].strip()
        m = re.match(r"\[(.+)\]", line)
        if m:
            cur = {"__name": m.group(1).upper()}
            secs.append(cur)
        elif cur is not None and "=" in line:
            k, v = line.split("=", 1)
            cur[k.strip().lower()] = v.strip().strip('"')
    return secs


def lods(xml_path):
    text = open(xml_path, encoding="utf-8", errors="replace").read()
    return [os.path.join(os.path.dirname(xml_path), f) for f in re.findall(r'ModelFile="([^"]+)"', text)]


def assemble(pkg, preset_cfg_dir, kind, lod_pref):
    """Walk attached_objects.cfg recursively. Returns (parts, merged_node_files)."""
    parts, merged, seen = [], [], set()

    def visit(cfg, inherited):
        if not os.path.exists(cfg) or cfg in seen:
            return
        seen.add(cfg)
        for s in cfg_sections(cfg):
            name = s["__name"]
            if name.startswith("MERGE_MODEL"):
                if s.get("merge_to_model", inherited) == kind and "merge_file" in s:
                    merged.append(os.path.join(pkg, s["merge_file"].replace("/", "\\")))
            elif name.startswith("SIM_ATTACHMENT"):
                k = s.get("attach_to_model", inherited)
                root = os.path.join(pkg, s.get("attachment_root", "").replace("/", "\\"))
                if k == kind and "attachment_file" in s:
                    xml = os.path.join(root, s["attachment_file"].replace("/", "\\"))
                    if os.path.exists(xml):
                        L = lods(xml)
                        if L:
                            off = tuple(float(v) for v in s["attach_offset"].split(",")) if "attach_offset" in s else None
                            parts.append((L[min(lod_pref, len(L) - 1)], s.get("attach_to_node"), os.path.basename(xml), off))
                visit(os.path.join(root, "config", "attached_objects.cfg"), k)
    visit(os.path.join(preset_cfg_dir, "attached_objects.cfg"), kind)
    return parts, merged


# ---------------------------------------------------------------- glTF loading

def load_gltf(path):
    g = json.load(open(path, encoding="utf-8"))
    nodes = g.get("nodes", [])
    parent = {c: i for i, n in enumerate(nodes) for c in n.get("children", [])}
    cache = {}

    def world(i):
        if i in cache:
            return cache[i]
        m = local_matrix(nodes[i])
        if i in parent:
            m = mat_mul(world(parent[i]), m)
        cache[i] = m
        return m
    return g, nodes, world


def attach_matrix(mats, node, offset):
    """World matrix for an attachment: its attach node (if any) times its attach_offset translation."""
    m = mats.get(node) if node else None
    if offset:
        T = [[1, 0, 0, offset[0]], [0, 1, 0, offset[1]], [0, 0, 1, offset[2]], [0, 0, 0, 1]]
        m = mat_mul(m, T) if m else T
    return m


def node_mats(files):
    out = {}
    for f in files:
        if not os.path.exists(f):
            continue
        g, nodes, world = load_gltf(f)
        for i, n in enumerate(nodes):
            out.setdefault(n.get("name", ""), world(i))
    return out


def xf(m, v):
    return (m[0][0] * v[0] + m[0][1] * v[1] + m[0][2] * v[2] + m[0][3],
            m[1][0] * v[0] + m[1][1] * v[1] + m[1][2] * v[2] + m[1][3],
            m[2][0] * v[0] + m[2][1] * v[1] + m[2][2] * v[2] + m[2][3])


def det3(m):
    return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
            + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))


def mat_class(g, mi):
    """'skip' for invisible/decal/glass, else ('opaque', double_sided)."""
    if mi is None:
        return "opaque", False
    m = g["materials"][mi]
    ext = " ".join(m.get("extensions", {}).keys()).lower()
    if "invisible" in ext or "geometry_decal" in ext or "glass" in ext or "windshield" in ext or "occluder" in ext or re.search(r"glass|cabing|window_?pane", m.get("name", ""), re.I):
        return "skip", False
    if m.get("alphaMode") == "BLEND" and "decal" in m.get("name", "").lower():
        return "skip", False
    return "opaque", bool(m.get("doubleSided")) or "flip_back_face" in ext


def matlabel(g, mi):
    if mi is None:
        return "-"
    m = g["materials"][mi]
    return f"{m.get('name', '?')} [{m.get('alphaMode', 'OPAQUE')}] " + ",".join(k.replace("ASOBO_material_", "") for k in m.get("extensions", {}))


def load_tris(path, attach, cls, spheres, out, skip_names=r"collision|occluder|drone|glass|window_?pane"):
    # "window_?pane", not "pane": a bare "pane" also dropped PMDG 777 "cabin_wall_panel" side walls and Fenix "Wall_Panel"s
    """Append triangles (v0, e1, e2, cls, double_sided) whose AABB touches any sphere (cx,cy,cz,r)."""
    if not os.path.exists(path):
        return 0
    g, nodes, world = load_gltf(path)
    bins, n_added = {}, 0
    pos_cache, idx_cache = {}, {}

    def fileof(bi):
        if bi not in bins:
            bins[bi] = open(os.path.join(os.path.dirname(path), g["buffers"][bi]["uri"]), "rb")
        return bins[bi]

    def positions(ai):
        """Raw float tuples of a POSITION accessor (shared buffers are read once)."""
        if ai not in pos_cache:
            acc = g["accessors"][ai]
            bv = g["bufferViews"][acc["bufferView"]]
            stride = bv.get("byteStride", 12)
            f = fileof(bv["buffer"])
            f.seek(bv.get("byteOffset", 0) + acc.get("byteOffset", 0))
            raw = f.read(stride * (acc["count"] - 1) + 12)
            if stride == 12:
                flat = struct.unpack("<%df" % (acc["count"] * 3), raw[:acc["count"] * 12])
                pos_cache[ai] = [flat[k:k + 3] for k in range(0, len(flat), 3)]
            else:
                pos_cache[ai] = [struct.unpack_from("<3f", raw, k * stride) for k in range(acc["count"])]
        return pos_cache[ai]

    def indices(ai):
        if ai not in idx_cache:
            ia = g["accessors"][ai]
            ibv = g["bufferViews"][ia["bufferView"]]
            f = fileof(ibv["buffer"])
            f.seek(ibv.get("byteOffset", 0) + ia.get("byteOffset", 0))
            code, size = {5121: ("B", 1), 5123: ("H", 2), 5125: ("I", 4)}[ia["componentType"]]
            idx_cache[ai] = struct.unpack("<%d%s" % (ia["count"], code), f.read(ia["count"] * size))
        return idx_cache[ai]

    for i, n in enumerate(nodes):
        if "mesh" not in n or re.search(skip_names, n.get("name", ""), re.I):
            continue
        W = mat_mul(attach, world(i)) if attach else world(i)
        flip = det3(W) < 0
        for p in g["meshes"][n["mesh"]]["primitives"]:
            if p.get("mode", 4) != 4:
                continue
            mc, ds = mat_class(g, p.get("material"))
            if mc == "skip":
                continue
            acc = g["accessors"][p["attributes"]["POSITION"]]
            if acc["componentType"] != 5126:
                continue
            # cull by the (shared) accessor AABB first
            mn, mx = acc["min"], acc["max"]
            corners = [xf(W, (a, b, c)) for a in (mn[0], mx[0]) for b in (mn[1], mx[1]) for c in (mn[2], mx[2])]
            lo = [min(c[k] for c in corners) for k in range(3)]
            hi = [max(c[k] for c in corners) for k in range(3)]
            near = [s for s in spheres if all(lo[k] - s[3] <= s[k] <= hi[k] + s[3] for k in range(3))]
            if not near:
                continue
            # MSFS optimized assets pack several primitives into one buffer: honour their ranges
            ap = p.get("extras", {}).get("ASOBO_primitive", {}) or p.get("extensions", {}).get("ASOBO_primitive", {})
            base = ap.get("BaseVertexIndex", 0)
            raw_pos = positions(p["attributes"]["POSITION"])
            if "indices" in p:
                allidx = indices(p["indices"])
                start = ap.get("StartIndex", 0)
                count = ap.get("PrimitiveCount", (len(allidx) - start) // 3) * 3
                idx = allidx[start:start + count]
            else:
                idx = range(len(raw_pos))
            vmemo = {}

            def V(k):
                v = vmemo.get(k)
                if v is None:
                    v = vmemo[k] = xf(W, raw_pos[base + k])
                return v
            for t in range(0, len(idx) - 2, 3):
                a, b, c = V(idx[t]), V(idx[t + 1]), V(idx[t + 2])
                if flip:
                    b, c = c, b
                tlo = (min(a[0], b[0], c[0]), min(a[1], b[1], c[1]), min(a[2], b[2], c[2]))
                thi = (max(a[0], b[0], c[0]), max(a[1], b[1], c[1]), max(a[2], b[2], c[2]))
                if not any(all(tlo[k] - s[3] <= s[k] <= thi[k] + s[3] for k in range(3)) for s in near):
                    continue
                e1 = (b[0] - a[0], b[1] - a[1], b[2] - a[2])
                e2 = (c[0] - a[0], c[1] - a[1], c[2] - a[2])
                out.append((a, e1, e2, cls, ds, tlo, thi, os.path.basename(path) + ":" + n.get("name", "") + " | " + matlabel(g, p.get("material"))))
                n_added += 1
    return n_added


# ---------------------------------------------------------------- acceleration grid + ray casting

class Grid:
    def __init__(self, tris, cell):
        self.tris, self.cell, self.cells = tris, cell, {}
        for i, t in enumerate(tris):
            lo, hi = t[5], t[6]
            i0, j0, k0 = (int(math.floor(lo[a] / cell)) for a in range(3))
            i1, j1, k1 = (int(math.floor(hi[a] / cell)) for a in range(3))
            for x in range(i0, i1 + 1):
                for y in range(j0, j1 + 1):
                    for z in range(k0, k1 + 1):
                        self.cells.setdefault((x, y, z), []).append(i)

    def cast(self, o, d, tmax, cull_back=False):
        """First hit (t, tri, backface) along ray o + t d (|d| = 1)."""
        c = self.cell
        ix, iy, iz = (int(math.floor(o[a] / c)) for a in range(3))
        step, tdelta, tnext = [], [], []
        for a, i in zip(range(3), (ix, iy, iz)):
            if d[a] > 1e-12:
                step.append(1); tdelta.append(c / d[a]); tnext.append(((i + 1) * c - o[a]) / d[a])
            elif d[a] < -1e-12:
                step.append(-1); tdelta.append(-c / d[a]); tnext.append((i * c - o[a]) / d[a])
            else:
                step.append(0); tdelta.append(1e30); tnext.append(1e30)
        best, tested, t_cell = None, set(), 0.0
        tris, cells = self.tris, self.cells
        dx, dy, dz = d
        while t_cell <= tmax:
            lst = cells.get((ix, iy, iz))
            if lst:
                for ti in lst:
                    if ti in tested:
                        continue
                    tested.add(ti)
                    v0, e1, e2 = tris[ti][0], tris[ti][1], tris[ti][2]
                    px = dy * e2[2] - dz * e2[1]; py = dz * e2[0] - dx * e2[2]; pz = dx * e2[1] - dy * e2[0]
                    det = e1[0] * px + e1[1] * py + e1[2] * pz
                    if -1e-12 < det < 1e-12:
                        continue
                    if cull_back and det > 0:
                        continue
                    inv = 1.0 / det
                    sx = o[0] - v0[0]; sy = o[1] - v0[1]; sz = o[2] - v0[2]
                    u = (sx * px + sy * py + sz * pz) * inv
                    if u < 0 or u > 1:
                        continue
                    qx = sy * e1[2] - sz * e1[1]; qy = sz * e1[0] - sx * e1[2]; qz = sx * e1[1] - sy * e1[0]
                    v = (dx * qx + dy * qy + dz * qz) * inv
                    if v < 0 or u + v > 1:
                        continue
                    t = (e2[0] * qx + e2[1] * qy + e2[2] * qz) * inv
                    if 1e-5 < t <= tmax and (best is None or t < best[0]):
                        best = (t, ti, det > 0)  # PMDG/Asobo meshes: front faces are clockwise
            tmin_next = min(tnext)
            if best is not None and best[0] <= tmin_next:
                return best
            if tnext[0] == tmin_next:
                ix += step[0]; t_cell = tnext[0]; tnext[0] += tdelta[0]
            elif tnext[1] == tmin_next:
                iy += step[1]; t_cell = tnext[1]; tnext[1] += tdelta[1]
            else:
                iz += step[2]; t_cell = tnext[2]; tnext[2] += tdelta[2]
        return best


# ---------------------------------------------------------------- cameras

def read_cameras(path, eye):
    """eye = (lon_m, lat_m_rightpos, vert_m). Returns {title: (pos_gltf, f, r, u, zoom)}."""
    text = open(path, encoding="utf-8").read()
    cams = {}
    for block in re.split(r"\[CAMERADEFINITION\.\d+\]", text)[1:]:
        title = re.search(r'Title="([^"]*)"', block).group(1)
        x, y, z = (float(v) for v in re.search(r"InitialXyz=\s*([^\r\n]+)", block).group(1).split(","))
        p, b, h = (math.radians(float(v)) for v in re.search(r"InitialPbh=\s*([^\r\n]+)", block).group(1).split(","))
        zoom = float(re.search(r"InitialZoom=\s*([-\d.]+)", block).group(1))
        cams[title] = camera((x, y, z), (p, h), eye, zoom)
    return cams


def camera(rel, ph, eye, zoom):
    x, y, z = rel
    p, h = ph
    pos = (-(x + eye[1]), y + eye[2], z + eye[0])                      # glTF frame: +x = left
    fr = (math.sin(h) * math.cos(p), math.sin(p), math.cos(h) * math.cos(p))   # right-positive frame
    rr = (math.cos(h), 0.0, -math.sin(h))
    ur = (-math.sin(h) * math.sin(p), math.cos(p), -math.cos(h) * math.sin(p))
    g = lambda v: (-v[0], v[1], v[2])
    return pos, g(fr), g(rr), g(ur), zoom


def hfov_for(zoom):
    # Calibrated on in-sim screenshots: zoom 0.44 shows ~84 deg across a 16:9 frame, and zoom 2.577
    # widened the 777 GoPro by a tan-ratio of 1.67 -> tan(half-angle) scales with zoom ** 0.289.
    return 2 * math.atan(math.tan(math.radians(HFOV_044) / 2) * (zoom / 0.44) ** 0.289)


HFOV_044 = 84.0

# ---------------------------------------------------------------- rendering

PALETTE = [(150, 190, 235), (110, 120, 90), (200, 200, 205), (245, 245, 250), (170, 160, 150), (60, 60, 70),
           (120, 100, 80), (230, 30, 30), (240, 0, 240)]
NAMES = ["sky", "ground", "airframe", "engine", "cabin", "seat", "cockpit", "backface", "too-close"]


def trace(gin, gext, o, d, ground_y):
    hit = gin.cast(o, d, R_INT) if gin else None
    if hit:
        t, ti, back = hit
        tri = gin.tris[ti]
        if t < NEAR:
            return 8, t
        if back and not tri[4]:
            return 7, t
        return tri[3], t
    if gext:
        h2 = gext.cast(o, d, 120.0, cull_back=True)
        if h2:
            return gext.tris[h2[1]][3], h2[0]
    if d[1] < -1e-6:
        return 1, (ground_y - o[1]) / d[1]
    return 0, 1e9


def render(cam, gin, gext, ground_y, w=96, h=54):
    pos, f, r, u, zoom = cam
    hf = hfov_for(zoom)
    th = math.tan(hf / 2)
    tv = th * h / w
    img, counts, core = [], [0] * 9, [0] * 9
    for j in range(h):
        row = []
        sy = 1 - 2 * (j + 0.5) / h
        for i in range(w):
            sx = 2 * (i + 0.5) / w - 1
            d = tuple(f[k] + sx * th * r[k] + sy * tv * u[k] for k in range(3))
            n = math.sqrt(d[0] ** 2 + d[1] ** 2 + d[2] ** 2)
            d = (d[0] / n, d[1] / n, d[2] / n)
            c, t = trace(gin, gext, pos, d, ground_y)
            row.append(c)
            counts[c] += 1
            if abs(sx) < 0.5 and abs(sy) < 0.5:
                core[c] += 1
        img.append(row)
    return img, counts, core


def enclosure(cam, gin, n=160):
    """Fraction of all-around rays whose first hit is a backface (camera inside something)."""
    pos = cam[0]
    back = total = 0
    ga = math.pi * (3 - math.sqrt(5))
    for k in range(n):
        y = 1 - 2 * (k + 0.5) / n
        rad = math.sqrt(1 - y * y)
        d = (math.cos(ga * k) * rad, y, math.sin(ga * k) * rad)
        hit = gin.cast(pos, d, 1.5) if gin else None
        if hit:
            total += 1
            if hit[2] and not gin.tris[hit[1]][4]:
                back += 1
    return back / n


def write_png(path, img, scale=4):
    h, w = len(img), len(img[0])
    raw = bytearray()
    for row in img:
        line = bytearray([0])
        for c in row:
            line += bytes(PALETTE[c]) * scale
        raw += bytes(line) * scale
    def chunk(tag, data):
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xffffffff)
    png = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w * scale, h * scale, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(bytes(raw), 9)) + chunk(b"IEND", b"")
    open(path, "wb").write(png)
