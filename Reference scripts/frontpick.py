"""Pick and write the engine-front views (Alt+1/5) from the search logs of front320.py / frontall.py.

Rule: among clear views (nothing blocking, centre looking outside, at least MIN_ENGINE % engine in the middle half),
take the clearest view of the engine whose angle off the inlet axis is inside BAND; if none, the clear view nearest
TARGET. Positions are rebuilt exactly (window z from the logs' 2-decimal values matched to the model's window list);
heading and pitch come from the log (whole degrees).
Usage: frontpick.py <log> [<log> ...] [--band 50,60] [--write]
"""
import json, math, os, re, sys
S = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, S)
import viewcheck as vc  # noqa: E402
from front320 import rewrite  # noqa: E402

ROAM = os.path.expandvars(r"%APPDATA%\Microsoft Flight Simulator 2024\SimObjects\Airplanes")
BAND = tuple(float(v) for v in sys.argv[sys.argv.index("--band") + 1].split(",")) if "--band" in sys.argv else (50.0, 60.0)
TARGET, MIN_ENGINE = sum(BAND) / 2, 10.0
HEAD = re.compile(r"^== (?P<name>[^:]+): .*?(?:glass \|x\| (?P<glass>[\d.]+))?")
ROW = re.compile(r"Alt\+(?P<s>[15]) z (?P<z>[+-][\d.]+) \((?P<ahead>[+-][\d.]+) m vs lip\), (?P<ins>[\d.]+) m in: +(?P<ang>[\d.]+) deg off the inlet axis \| "
                 r"hdg (?P<h>[+-]\d+) pitch (?P<p>[+-]\d+): outside (?P<out>\d+)% wing/engine (?P<we>\d+)% engine (?P<eng>\d+)% bad (?P<bad>\d+)% centre (?P<c>\w+)")
FILES = {}   # filled from the adapters, see files_for()


def fam737(name):
    return "737-800" if ("-800" in name or "BBJ2" in name) else "737-900" if "-900" in name else "737-700"


def files_for(name):
    if name.startswith("PMDG 737"):
        return [os.path.join(ROAM, f"PMDG {fam737(name)}", "presets", "pmdg", q, "config", "cameras.CFG") for q in (name, name.replace(" BW", " SSW"))]
    if name.startswith("FNX_"):
        p = name.split("_")
        return [os.path.join(ROAM, "FNX_32X", "presets", "fnx", "_".join(["FNX", p[1], e, w] + p[4:]), "config", "cameras.cfg")
                for e in ("CFM", "IAE") for w in ("SL", "WF")]
    return {"FBW": [os.path.join(ROAM, "FlyByWire_A320_NEO", "cameras.CFG")],
            "777-200ER": [os.path.join(ROAM, rf"PMDG 777-200ER\presets\pmdg\PMDG 777-200ER {e}\config\cameras.CFG") for e in ("PW", "GE", "RR")]
                         + [os.path.join(ROAM, r"PMDG 777F\presets\pmdg\PMDG 777F\config\cameras.CFG")],
            "777-300ER": [os.path.join(ROAM, r"PMDG 777-300ER\presets\pmdg\PMDG 777-300ER\config\cameras.CFG")],
            "iFly 189": [os.path.join(ROAM, "iFly 737-MAX8-189Seats", "cameras.CFG")],
            "iFly 178": [os.path.join(ROAM, "iFly 737-MAX8", "cameras.CFG")],
            "iFly 166": [os.path.join(ROAM, "iFly 737-MAX8-166Seats", "cameras.CFG")],
            "iFly 8200": [os.path.join(ROAM, "iFly 737-MAX8200", "cameras.CFG")]}[name]


EYES = {"FNX_319": (38.650528, -1.623061, 3.955627), "FNX_320": (43.920738, -1.623061, 3.955627), "FNX_321": (57.965850, -1.623061, 3.955627),
        "FBW": (43.72074, -1.723061, 4.355627), "777-200ER": (82.122316, -1.74, 7.722), "777-300ER": (99.559998, -1.74, 7.722),
        "iFly": (49.683998, -1.63, 2.1)}
CAM_Y = {"FNX": 1.72}


def eye_of(name):
    if name.startswith("PMDG 737"):
        return tuple(v * vc.FT for v in {"737-700": (37.31212336, -1.66, 3.909), "737-800": (47.07464336, -1.66, 3.909),
                                         "737-900": (52.13864336, -1.66, 3.909)}[fam737(name)])
    key = name[:7] if name.startswith("FNX_") else "iFly" if name.startswith("iFly") else name
    return tuple(v * vc.FT for v in EYES[key])


def parse(paths):
    blocks, cur = {}, None
    for path in paths:
        for line in open(path, encoding="utf-8", errors="replace"):
            line = line.rstrip()
            if line.startswith("== "):
                cur = line[3:].split(":")[0]
                g = re.search(r"glass \|x\| ([\d.]+)", line)
                cy = re.search(r"cam y ([+-][\d.]+)", line)
                blocks[cur] = {"glass": float(g.group(1)) if g else None, "cam_y": float(cy.group(1)) if cy else None, "rows": []}
            elif cur and (m := ROW.search(line)):
                blocks[cur]["rows"].append({k: (v if k in ("c",) else float(v)) for k, v in m.groupdict().items()})
    return blocks


def main():
    logs = [a for a in sys.argv[1:] if a.endswith(".log")]
    out = {}
    only = sys.argv[sys.argv.index("--only") + 1].split(",") if "--only" in sys.argv else None
    for name, b in parse(logs).items():
        if only and name not in only:
            continue
        eye = eye_of(name)
        if b["glass"] is None:   # front320 Fenix/FBW logs: glass from the model
            if name == "FBW":
                b["glass"], b["cam_y"] = 1.95, 4.355627 * vc.FT + 0.73
            else:
                import fnxcheck as fx
                b["glass"], b["cam_y"] = fx.windows(name)[1], CAM_Y["FNX"]
        picks = {}
        for s in "15":
            rows = [r for r in b["rows"] if int(r["s"]) == int(s)]
            ok = [r for r in rows if r["bad"] <= 5 and r["eng"] >= MIN_ENGINE and r["c"] in ("sky", "ground", "airframe", "engine")]
            band = [r for r in ok if BAND[0] <= r["ang"] <= BAND[1]]
            score = lambda r: 2.0 * r["eng"] + 0.3 * r["we"] + 0.2 * r["out"] - 3 * r["bad"]
            pick = max(band, key=score) if band else min(ok, key=lambda r: (abs(r["ang"] - TARGET), -score(r))) if ok else None
            if pick:
                sign = -1 if s == "1" else 1
                x_abs = b["glass"] - pick["ins"]
                pos = (sign * x_abs, b["cam_y"], pick["z"])
                xyz = [pos[0] - eye[1], pos[1] - eye[2], pos[2] - eye[0]]
                picks[s] = {"xyz": [round(v, 6) for v in xyz], "pbh": [pick["p"], 0.0, pick["h"]], "z": pick["z"], "angle": pick["ang"],
                            "ahead_of_lip": pick["ahead"], "inset": pick["ins"], "engine_pct": pick["eng"], "outside_pct": pick["out"],
                            "in_band": bool(band)}
        out[name] = picks
        for s, v in picks.items():
            print(f"{name:18s} Alt+{s}: z {v['z']:+.2f} ({v['ahead_of_lip']:+.2f} m vs lip), {v['inset']:.2f} m in, {v['angle']:.1f} deg"
                  f"{'' if v['in_band'] else ' (outside the band: best clear view)'}, hdg {v['pbh'][2]:+.0f} pitch {v['pbh'][0]:+.0f}, "
                  f"engine {v['engine_pct']:.0f}% outside {v['outside_pct']:.0f}%")
        if "--write" in sys.argv and len(picks) == 2:
            # keep the previous slot 1/5 values (data only, for a restore on request), then rewrite those two blocks
            oldp = os.path.join(S, "old_engine_front.json")
            old = json.load(open(oldp)) if os.path.exists(oldp) else {}
            for f in files_for(name):
                key = os.path.relpath(f, ROAM)
                if key not in old:
                    text = open(f, encoding="utf-8").read()
                    old[key] = {s: {k: re.search(r'Title="%s".*?%s=\s*([^\r\n]+)' % (s, k), text, re.S).group(1)
                                    for k in ("InitialXyz", "InitialPbh")} for s in "15"}
                print(f"    wrote {key}: {rewrite(f, picks)}")
            json.dump(old, open(oldp, "w"), indent=1)
    json.dump(out, open(os.path.join(S, "frontpick.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
