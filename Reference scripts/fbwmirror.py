"""Mirror the FlyByWire left-side cabin views to the right and confirm the mirrored seats see out (no lining/
interior in view). Right-wing triangles get culled in this checker, so only 'outside' and 'bad' are trusted there.
Usage: fbwmirror.py [--write]
"""
import json, math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import viewcheck as vc  # noqa: E402
import genclassic as gc  # noqa: E402
import genviews as gv  # noqa: E402

ac = gc.fbw(None)
eye = ac["eye"]
cache = os.path.join(ac["png_dir"], "views.json")
views = {k: [list(v[0]), list(v[1]), v[2]] for k, v in json.load(open(cache)).items()}
for left, right in (("1", "5"), ("2", "6"), ("3", "7"), ("4", "8")):
    (x, y, z), (p, b, h), zoom = views[left]
    lat_abs = x + eye[1]                        # right-positive lateral of the left seat (negative)
    views[right] = [[-lat_abs - eye[1], y, z], [p, b, -h], zoom]
pseudo = {s: vc.camera(tuple(views[s][0]), (math.radians(views[s][1][0]), math.radians(views[s][1][2])), eye, views[s][2]) for s in "12345678"}
gin, gext, gy = ac["scene"](pseudo)
for s in "12345678":
    img, counts, core = vc.render(pseudo[s], gin, gext, gy)
    tot, ctot = sum(counts), sum(core)
    print(f"slot {s}: lat {views[s][0][0] + eye[1]:+.2f} z {views[s][0][2] + eye[0]:+.2f} hdg {views[s][1][2]:+.0f}: "
          f"outside {100 * sum(core[k] for k in (0, 1, 2, 3)) / ctot:.0f}% interior {100 * core[4] / ctot:.0f}% bad {100 * (counts[7] + counts[8]) / tot:.0f}% "
          f"centre {vc.NAMES[img[len(img) // 2][len(img[0]) // 2]]}")
if "--write" in sys.argv:
    json.dump(views, open(cache, "w"), indent=1)
    print("mirrored views saved to the cache")
