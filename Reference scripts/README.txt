These are the Python scripts used to build the views. They need Python 3 and nothing else.

The folder paths are written for one particular PC (D:\MSFS2024 Community\Community and the Steam user folder),
so change them before running anything. The first few lines of each script explain what it does.

nodes.py: glTF node transforms (local and world matrices).
viewcheck.py: Core offline checker: assembles PMDG models, loads triangles (honouring ASOBO_primitive ranges), ray casts views, renders small PNGs.
checkrun.py: Runs the checker on one PMDG preset's camera file and reports each view.
batch.py: The PMDG presets and eyepoints the PMDG tools work through.
gen777.py: Writes 777 view files from the 200ER set with per-variant adjustments.
gen737.py: Writes 737 view files from the models (window centres, windshield position).
autofix.py: Searches nearby seats for PMDG views that fail the check and rewrites them.
fnxcheck.py: Fenix model assembly (two packages, attach nodes, Template/MergeModel LODs) plus checker.
genfnx.py: Fenix seat search and file writer (one search per cabin layout, copied to engine/wingtip twins).
genviews.py: Shared seat search used for the single-model aircraft.
genclassic.py: iFly and FlyByWire adapters (windows, engines, masked skins, window lining) and writer.
gen757.py: BlueBird 757-200 adapter and writer: datum offset, windows, engines, wing root, one scene load per run, engine-front pick, seat rows (both sides paired), twins (winglets, four-door, no cabin).
wsray.py: Finds the front windshield by ray casting straight ahead from the pilot's eye.
fixgopro.py: Moves only the GoPro block to 12 cm inside the windshield.
fbwmirror.py: Mirrors FlyByWire left-side seats to the right and checks them.
tweakifly.py: The iFly engine-front tweak (same window, closer to the glass, more aft-looking).
fnxsound.py: Read-only list of where the Fenix places its sounds.
seatrows.py: Read-only: counts each cabin's seat rows and gives every cabin view its seat (for example 12A).
front320.py: Engine-front search for the Fenix and FlyByWire: windows ranked by angle off the inlet axis, then a clear view of the intake.
frontall.py: The same engine-front search for the PMDG 777s and the iFly.
frontpick.py: Picks the engine-front seat from those search logs (50 to 60 degrees, clearest view) and rewrites only slots 1 and 5.
anchors.py: Read-only: where the iFly and FlyByWire anchor their sounds (sound.xml node names to model positions).
probe.py: Lists mesh nodes matching a pattern with world bounding boxes and materials.
bbox.py: Overall bounding box of a model or of matching meshes.
mats.py: Lists a model's materials and how often each is used.
