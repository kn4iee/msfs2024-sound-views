"""Move only the GoPro camera (Title "0") to 12 cm inside the front windshield, measured by ray cast from the
pilot's eye straight ahead at 0.25 m left of centre. Edits InitialXyz z of that one block; everything else is kept
byte-for-byte (CRLF included). Also updates the generators' cached views so a rerun keeps the fix.
Usage: fixgopro.py [--write]
"""
import glob, json, os, re, sys

ROAM = os.path.expandvars(r"%APPDATA%\Microsoft Flight Simulator 2024\SimObjects\Airplanes")
VC = os.path.join(os.path.dirname(__file__), "vc")
# glass distance ahead of the pilot eye (m, ray cast) and the pilot view's rel z, per type
FIX = {"319": (0.79, -2.484581), "320": (0.82, -2.506579), "321": (0.78, -2.455647), "fbw": (0.76, -2.274009)}
WRITE = "--write" in sys.argv


def new_z(kind):
    dist, pilot_z = FIX[kind]
    return pilot_z + dist - 0.12


def patch(path, z):
    raw = open(path, "rb").read()
    text = raw.decode("utf-8")
    m = re.search(r'(\[CAMERADEFINITION\.\d+\]\r?\nTitle="0".*?InitialXyz=\s*)([-\d.]+),\s*([-\d.]+),\s*([-\d.]+)', text, re.S)
    if not m:
        return f"no GoPro block in {path}"
    old = float(m.group(4))
    text2 = text[:m.start(2)] + f"{float(m.group(2)):.6f}, {float(m.group(3)):.6f}, {z:.6f}" + text[m.end(4):]
    if WRITE:
        open(path, "wb").write(text2.encode("utf-8"))
    return f"{os.path.relpath(path, ROAM)}: GoPro z {old:+.3f} -> {z:+.3f}"


for f in sorted(glob.glob(os.path.join(ROAM, "FNX_32X", "presets", "fnx", "FNX_*", "config", "cameras.cfg"))):
    print(patch(f, new_z(os.path.basename(os.path.dirname(os.path.dirname(f)))[4:7])))
print(patch(os.path.join(ROAM, "FlyByWire_A320_NEO", "cameras.CFG"), new_z("fbw")))
# keep the cached search results in step
for cache in glob.glob(os.path.join(VC, "fnx_new", "*", "views.json")) + [os.path.join(VC, "fbw_new", "views.json")]:
    kind = "fbw" if "fbw_new" in cache else os.path.basename(os.path.dirname(cache))[4:7]
    v = json.load(open(cache))
    v["0"][0][2] = new_z(kind)
    if WRITE:
        json.dump(v, open(cache, "w"), indent=1)
print("written" if WRITE else "dry run")
