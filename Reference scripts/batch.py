"""Run checkrun.py for one preset per distinct cabin layout; collect the reports."""
import json, os, subprocess, sys, time

S = os.path.dirname(os.path.abspath(__file__))
C = r"D:\MSFS2024 Community\Community"
R = os.path.expandvars(r"%APPDATA%\Microsoft Flight Simulator 2024\SimObjects\Airplanes")
RUNS = [
    ("777-300ER", "pmdg-aircraft-77w", "PMDG 777-300ER", "PMDG 777-300ER", 99.559998, -1.74, 7.722),
    ("777F", "pmdg-aircraft-77f", "PMDG 777F", "PMDG 777F", 82.122316, -1.74, 7.722),
] + [
    (f"737-700 {p}", "pmdg-aircraft-737", "PMDG 737-700", p, 37.31212336, -1.66, 3.909)
    for p in ("PMDG 737-700 BW SC", "PMDG 737-700 BW TC", "PMDG 737-700BDSF BW", "PMDG 737-BBJ BW")
] + [
    (f"737-800 {p}", "pmdg-aircraft-738", "PMDG 737-800", p, 47.07464336, -1.66, 3.909)
    for p in ("PMDG 737-800 BW HD", "PMDG 737-800 BW SC", "PMDG 737-800 BW TC", "PMDG 737-800BCF BW", "PMDG 737-800BDSF BW", "PMDG 737-BBJ2 BW")
] + [
    (f"737-900 {p}", "pmdg-aircraft-739", "PMDG 737-900", p, 52.13864336, -1.66, 3.909)
    for p in ("PMDG 737-900 BW SC", "PMDG 737-900 BW TC", "PMDG 737-900ER BW HD", "PMDG 737-900ER BW SC", "PMDG 737-900ER BW TC")
]
def main():
    only = sys.argv[1:] or None
    allrep = {}
    os.makedirs(os.path.join(S, "vc"), exist_ok=True)
    for label, pkg, ac, preset, lon, lat, vert in RUNS:
        if only and not any(o in label for o in only):
            continue
        pdir = os.path.join(C, pkg, "SimObjects", "Airplanes", ac, "presets", "pmdg", preset)
        cams = os.path.join(R, ac, "presets", "pmdg", preset, "config", "cameras.CFG")
        out = os.path.join(S, "vc", preset.replace(" ", "_"))
        t0 = time.time()
        res = subprocess.run([sys.executable, "-I", os.path.join(S, "checkrun.py"), pdir, str(lon), str(lat), str(vert), cams, out,
                              "--slots", "0,1,2,3,4,5,6,7,8,9"], capture_output=True, text=True)
        warn = [l for l in res.stdout.splitlines() if l.startswith("  !")]
        try:
            allrep[label] = json.load(open(os.path.join(out, "report.json")))
        except OSError:
            allrep[label] = {"error": res.stderr[-800:]}
        print(f"== {label} ({time.time() - t0:.0f}s) {' '.join(warn)}", flush=True)
        for k, v in sorted(allrep[label].items()):
            print(f"   {k}: {v}", flush=True)
    json.dump(allrep, open(os.path.join(S, "vc", "all_reports.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
