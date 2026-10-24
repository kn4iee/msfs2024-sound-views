"""Write a 777 custom-camera file derived from the 200ER PW set.

Usage: gen777.py <source cameras.CFG> <target cameras.CFG> <new eyepoint lon ft> <slot=delta_m> ...
Slots not listed keep their eyepoint-relative position (cockpit views). Listed slots keep their
absolute fuselage position from the 200ER, shifted by delta_m (positive = toward the nose).
"""
import re, sys

src, dst, new_eye_ft = sys.argv[1], sys.argv[2], float(sys.argv[3])
deltas = {k: float(v) for k, v in (a.split("=") for a in sys.argv[4:])}
OLD_EYE = 82.122316 * 0.3048
NEW_EYE = new_eye_ft * 0.3048
text = open(src, encoding="utf-8").read()
blocks = re.split(r"(?=\[CAMERADEFINITION\.\d+\])", text)
out = []
for b in blocks:
    t = re.search(r'Title="([^"]*)"', b)
    if t and t.group(1) in deltas:
        m = re.search(r"InitialXyz=\s*([-\d.]+),\s*([-\d.]+),\s*([-\d.]+)", b)
        x, y, z = (float(v) for v in m.groups())
        z_abs = z + OLD_EYE + deltas[t.group(1)]
        b = b[:m.start()] + f"InitialXyz= {x:.6f}, {y:.6f}, {z_abs - NEW_EYE:.6f}" + b[m.end():]
        print(f"slot {t.group(1)}: lon {z + OLD_EYE:7.3f} -> {z_abs:7.3f} m (rel z {z_abs - NEW_EYE:8.3f})")
    out.append(b)
open(dst, "w", encoding="utf-8", newline="\r\n").write("".join(out).replace("\r\n", "\n"))
