"""Engine-front tweak for the iFly (Alt+1/5) on all four versions: keep each slot's window, choose the inset,
heading and pitch that show the intake best with nothing blocking, and rewrite only those two slots.
Usage: tweakifly.py [--write]
"""
import json, math, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
import viewcheck as vc  # noqa: E402
import genclassic as gc  # noqa: E402

WRITE = "--write" in sys.argv
INSETS, HDGS, PITCHES = (0.12, 0.15, 0.18, 0.22), (107, 112, 117, 122), (-25, -31)


def measure(cam, gin, gext, gy, w=48, h=27):
    img, counts, core = vc.render(cam, gin, gext, gy, w, h)
    tot, ctot = sum(counts), sum(core)
    return (100 * core[3] / ctot, 100 * sum(core[k] for k in (0, 1, 2, 3)) / ctot,
            100 * (counts[7] + counts[8]) / tot, img[h // 2][w // 2])


def patch_block(text, title, xyz, pbh):
    m = re.search(r'\[CAMERADEFINITION\.\d+\]\r?\nTitle="%s".*?(?=\[CAMERADEFINITION|\Z)' % title, text, re.S)
    blk = m.group(0)
    blk2 = re.sub(r"InitialXyz=\s*[^\r\n]+", "InitialXyz= {:.6f}, {:.6f}, {:.6f}".format(*xyz), blk)
    blk2 = re.sub(r"InitialPbh=\s*[^\r\n]+", "InitialPbh= {:.6f}, {:.6f}, {:.6f}".format(*pbh), blk2)
    return text[:m.start()] + blk2 + text[m.end():]


for variant in gc.IFLY_VARIANTS:
    ac = gc.ifly(variant)
    eye = ac["eye"]
    cache = os.path.join(ac["png_dir"], "views.json")
    views = json.load(open(cache))
    slots = {}
    for slot, sign in (("1", -1), ("5", 1)):
        (x, y, z), pbh, zoom = views[slot]
        slots[slot] = (sign, y, z, pbh, zoom)
    pseudo = {}
    for slot, (sign, y, z, pbh, zoom) in slots.items():
        for ins in INSETS:
            lat = sign * (ac["wall_x"] - ins)
            pseudo[f"{slot}-{ins}"] = vc.camera((lat - eye[1], y, z), (0, 0), eye, zoom)
    gin, gext, gy = ac["scene"](pseudo)
    changed = {}
    for slot, (sign, y, z, pbh, zoom) in slots.items():
        cur = measure(vc.camera((views[slot][0][0], y, z), (math.radians(pbh[0]), math.radians(pbh[2])), eye, zoom), gin, gext, gy)
        best = None
        for ins in INSETS:
            x = sign * (ac["wall_x"] - ins) - eye[1]
            for hdg in HDGS:
                for pitch in PITCHES:
                    r = measure(vc.camera((x, y, z), (math.radians(pitch), math.radians(sign * hdg)), eye, zoom), gin, gext, gy)
                    if r[2] > 5 or r[3] in (7, 8):
                        continue
                    sc = r[0] + 0.1 * r[1]
                    if best is None or sc > best[0]:
                        best = (sc, ins, hdg, pitch, r, x)
        if best and best[4][0] > cur[0] + 3:
            sc, ins, hdg, pitch, r, x = best
            changed[slot] = ([x, y, z], [float(pitch), 0.0, float(sign * hdg)])
            print(f"{variant} Alt+{slot}: window z {z + eye[0]:+.2f} kept; engine {cur[0]:.0f}% -> {r[0]:.0f}% "
                  f"(outside {r[1]:.0f}%, bad {r[2]:.0f}%): {ins:.2f} m in, hdg {sign * hdg:+d}, pitch {pitch}")
        else:
            print(f"{variant} Alt+{slot}: unchanged (engine {cur[0]:.0f}%; no clearly better unblocked seat)")
    if WRITE and changed:
        dst = ac["dst"]
        text = open(dst, "rb").read().decode("utf-8")
        for slot, (xyz, pbh) in changed.items():
            text = patch_block(text, slot, xyz, pbh)
            views[slot][0], views[slot][1] = xyz, pbh
        open(dst, "wb").write(text.encode("utf-8"))
        json.dump(views, open(cache, "w"), indent=1)
        chk = open(dst, "rb").read()
        print(f"    wrote {os.path.basename(os.path.dirname(dst))}: {chk.count(b'[CAMERADEFINITION.')} blocks, "
              f"CRLF {chk.count(b'\r\n')}/{chk.count(b'\n')}", flush=True)
