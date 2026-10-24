"""Print world-space positions of glTF nodes whose names match a regex."""
import json, re, sys
import math


def mat_mul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(4)) for j in range(4)] for i in range(4)]


def local_matrix(n):
    if "matrix" in n:
        m = n["matrix"]  # column-major
        return [[m[c * 4 + r] for c in range(4)] for r in range(4)]
    t = n.get("translation", [0, 0, 0])
    q = n.get("rotation", [0, 0, 0, 1])
    s = n.get("scale", [1, 1, 1])
    x, y, z, w = q
    r = [
        [1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
        [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
        [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)],
    ]
    return [
        [r[0][0] * s[0], r[0][1] * s[1], r[0][2] * s[2], t[0]],
        [r[1][0] * s[0], r[1][1] * s[1], r[1][2] * s[2], t[1]],
        [r[2][0] * s[0], r[2][1] * s[1], r[2][2] * s[2], t[2]],
        [0, 0, 0, 1],
    ]


def main():
    pattern = re.compile(sys.argv[1], re.I)
    for path in sys.argv[2:]:
        g = json.load(open(path, encoding="utf-8"))
        nodes = g.get("nodes", [])
        parent = {}
        for i, n in enumerate(nodes):
            for c in n.get("children", []):
                parent[c] = i

        def world(i):
            m = local_matrix(nodes[i])
            while i in parent:
                i = parent[i]
                m = mat_mul(local_matrix(nodes[i]), m)
            return m

        hits = [(i, n.get("name", "")) for i, n in enumerate(nodes) if pattern.search(n.get("name", ""))]
        if not hits:
            continue
        print("==", path.split("\\")[-1])
        for i, name in hits:
            m = world(i)
            x, y, z = m[0][3], m[1][3], m[2][3]
            print(f"  {name:45s} x={x:8.3f} y={y:7.3f} z={z:8.3f} m   (z_ft={z/0.3048:7.2f} lat_ft={x/0.3048:7.2f})")


if __name__ == "__main__":
    main()
