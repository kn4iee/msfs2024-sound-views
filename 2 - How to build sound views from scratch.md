# Building sound-tuned camera views from scratch

This is the full method used to give PMDG 777 and 737, Fenix A319, A320 and A321, FlyByWire A32NX and iFly 737 MAX 8 aircraft in Microsoft Flight Simulator 2024 a set of custom cabin views chosen for how they sound. It is written so the method can be repeated on any airliner. Views for the PMDG 737-600 and the TFDi MD-11 and MD-11F were made by wolfman1360 and added later; section 15 notes how each was checked. The BlueBird 757-200 was added after that, built and checked in the sim with this method. What changed after the first build, and why, is in [3 - Changelog.md](3%20-%20Changelog.md).

## 1. The idea

In MSFS the camera is the listener. Where the camera sits and which way it faces decides how loud each sound is and which ear it lands in. So a view built for sound is a seat: put the camera at a cabin window close to the part that makes the noise, facing the way a passenger would look at it.

Every aircraft gets the same layout, so muscle memory carries across fleets:

**The layout**

| Key | View | Aimed at |
| --- | --- | --- |
| Alt+1 (left), Alt+5 (right) | Engine front | A window seat a few rows in front of the engine intake, 50 to 60 degrees off the engine's forward axis, looking back into it: fan and buzzsaw noise. |
| Alt+2 (left), Alt+6 (right) | Over-wing | Just behind the wing root's leading edge: slats, the engine from close by, packs and hydraulics under the wing box. |
| Alt+3 (left), Alt+7 (right) | Wing | Over the middle of the wing: flaps, main gear and the hydraulic bay. |
| Alt+4 (left), Alt+8 (right) | Behind the wing | 1.5 to 2.5 metres behind the wing root's trailing edge, looking forward at it: exhaust roar where the sound set models it. |
| Alt+9 | Pilot seat | The aircraft's own pilot view (keep the existing one). |
| Alt+0 | Windshield GoPro | 12 cm inside the captain's front windshield at eye height, 25 cm left of centre, pitched 7.6 degrees down. |

## 2. Requirements

- MSFS 2024 with the aircraft installed. Default key bindings: Alt+0 to Alt+9 load a custom camera, Ctrl+Alt+0 to Ctrl+Alt+9 save one.
- Python 3. Everything here uses only the standard library: reading glTF files is JSON plus binary buffers.
- Optionally the reference scripts in this zip (folder `Reference scripts`). They were written for this PC, so their paths are hard-coded, but they show every step.

## 3. Find the view files

Custom views live in the sim's user folder, not in the aircraft package. On a Steam install that is `%APPDATA%\Microsoft Flight Simulator 2024\SimObjects\Airplanes\`.

- Modular MSFS 2024 aircraft (PMDG, Fenix): one file per preset, at `<aircraft folder>\presets\<developer>\<preset>\config\cameras.cfg`.
- Older single-model aircraft (FlyByWire, iFly): one file per aircraft folder, at `<aircraft folder>\cameras.CFG`.
- The sim writes the file when Ctrl+Alt+N is pressed and reads it only when the aircraft loads. Edit files only while that aircraft is not loaded, and reload it to see changes.
- Before replacing anything, read the existing file. Existing views may be worth keeping; copy the file first if so.

## 4. The file format

The file is a `[VERSION]` header followed by `[CAMERADEFINITION.N]` blocks with Windows (CRLF) line endings. The fields that matter:

**Camera block fields**

| Field | Meaning |
| --- | --- |
| `Title` | The slot: "0" to "9". Other titles (such as "Pilot") are not Alt slots; leave them alone. |
| `InitialXyz` | Position in metres relative to the aircraft's eyepoint: x right, y up, z forward. |
| `InitialPbh` | Pitch, bank, heading in degrees. Negative pitch looks down; negative heading looks left; 0 is straight ahead, 90 is square out to the right, 120 is 30 degrees behind square. |
| `InitialZoom` | Field of view. 0.354 was used for cabin views, 2.577 for the GoPro. Zoom 0.44 shows about 84 degrees across a 16:9 screen; tan(half-angle) scales with zoom to the power 0.289. |
| `Category`, `SubCategory` | `"Cockpit"` and `"Custom"`. Cockpit-category cameras count as inside views for sound. |

Copy all the other fields from an existing block (Guid, Origin "Virtual Cockpit", ClipMode and so on). Give each new block its own Guid.

## 5. Find the eyepoint and the model frame

1. Read `eyepoint = longitudinal, lateral, vertical` (feet from the reference datum) from the aircraft's `cameras.cfg` or `aircraft.cfg`. Camera positions are relative to this point.
2. Read `reference_datum_position` in `flight_model.cfg`. When it is 0,0,0 (true for every aircraft here except the 757), the datum is the 3D model's origin. Otherwise it is "the position of the Datum Reference Point relative to the model center" (MSFS SDK), in feet, in the order longitudinal, lateral, vertical; add it to the eyepoint. The BlueBird 757's is 86.82 ft forward, which puts its datum about 4 m ahead of the nose.
3. In the glTF model files, +x is the aircraft's left, +y is up and +z is forward. So model position = (-(x + eye lateral), y + eye vertical, z + eye longitudinal), with the eyepoint (datum offset included) converted to metres.
4. Do not assume the eyepoint is the pilot's head. The Fenix eyepoint sits 2.5 m ahead of its pilot camera. Take the pilot's real position from the aircraft's own pilot camera or from an existing pilot view.

## 6. Assemble the model

- Modular aircraft: start at the preset's `config\attached_objects.cfg` and follow every `[SIM_ATTACHMENT.N]` recursively, for the interior and exterior separately. Each part's `attachment_file` is a model XML listing its LODs.
- Place each part at its `attach_to_node`: that node's world matrix comes from parts loaded earlier, times any `attach_offset`. Parent parts load first.
- Model XMLs can use `<LODS Template="...">` and per-LOD `<MergeModel>` entries (the Fenix wings get their sharklets or fences this way). Follow both, or whole parts go missing.
- One aircraft can be split over several packages (Fenix A319/A321 parts reference A320-package parts). Resolve every path across all of the aircraft's packages, as the sim does.
- Single-model aircraft: `model\model.cfg` lists `normal=` (exterior) and `interior=` XMLs; each XML points to its glTF.
- Use LOD0 for cabin parts: lower LODs have no window holes. Seats can use a coarse LOD; they only need to block.
- MSFS-optimized glTFs share vertex buffers between primitives. Honour each primitive's `ASOBO_primitive` BaseVertexIndex, StartIndex and PrimitiveCount, or triangles get duplicated.
- Skip geometry the sim doesn't draw or that isn't normally there: invisible, collision and occluder materials, glass, decals, mouse-click shapes, and helper meshes (Fenix `Skel_*`). Also skip ground props such as engine covers, safety cones and chocks.

## 7. Measure the airframe

- **Windows:** find the cabin window glass meshes. Group their vertices along the fuselage to get one centre per window, plus the glass's distance from the centreline and the window's height. Make sure the mesh is the glass: iFly shades are parked above the windows when open, which gave a height 30 cm too high.
- **Engines:** the nacelle's forward-most point is the intake lip. Exclude engine covers and cones in front of the engine. Also measure the fan face (the front of the fan-blade mesh) and the engine axis: its distance out from the centreline and its height. The engine-front rule in step 9 needs all three.
- **Wing:** take wing vertices close to the fuselage. Their forward-most point is the root leading edge; their rearmost is the root trailing edge.
- **Main gear:** the gear attach point or bay.
- **Front windshield:** names can mislead. On the Fenix, `Fuselage_Windshield_Window_L` is the side window; the front pane is `Misc_Windshield_Captain` in the cockpit model. Measure it by casting a ray straight ahead from the pilot's eye, treating glass as solid.

## 8. Find the sound sources

- Sounds are defined in `sound.xml` files: one for the aircraft, plus one per part on modular aircraft (Fenix: engines, fuselage, wings, gear, cabin, cockpit). Read them; never edit them, and leave third-party sound packs untouched.
- Each `<Sound>` is anchored by `NodeName` (a node in that part's model), `ReferencePointName` or nothing, plus optional PositionX/Y/Z offsets. Convert each anchor to the model frame to see where it plays.
- The `ViewPoint` attribute decides what is heard from the cabin. Cabin views are inside views: they play `All` and `Inside` sounds, never `Outside` ones such as exterior wind, brakes or gear-door loops. Place views for the sounds that can actually be heard.
- Directional layers (an engine's front intake sound versus its rear exhaust roar) may be set in the sound.xml (ConeHeading) or hidden inside the Wwise package. The behind-the-wing view only pays off when the set has rear layers. On the Fenix all engine sound comes from one point mid-engine, so that view is the quiet seat.
- A sound with no NodeName at all plays at the aircraft's datum (MSFS SDK). On the iFly the hydraulic and flap sounds have none, so they play over the wing. Where the datum isn't the model origin (step 5), that can be far from the wing: on the 757 it is ahead of the nose.
- Don't present guesses about the sim as fact. Where a sound plays when its NodeName is set but missing from the model was never verified; listening in the sim is the final test.
- Write the anchors down per aircraft. On this project:
  - Fenix: one engine point mid-nacelle; PTU and packs at the datum, over the wing box; slats beside the over-wing view; flaps and main gear under the wing view.
  - FlyByWire: each engine at its fan, with separate front and rear layers. The PTU and electric pumps sit 1.8 m behind the datum, the slats on the right side only, and the flap motor beside the left behind-the-wing seat.
  - iFly: each engine at its fan, with front and rear layers.
  - Boris Audio Works 737 (the same files on the 737-600 and 737-700): electric hydraulic pumps under the wing views; flaps with no node, so they play at the datum.
  - TFDi MD-11 (Echo19 Audio sounds, plus the aek sound MD-11 pack where installed): each wing engine at one point at the back of the engine, about 8.4 m out from the centreline; the tail engine and the APU in the tail. The hydraulic pumps, flaps, gear and touchdowns have no node, so they play at the datum, on the centreline about 3 m behind the over-wing seats. The packs play at the forward door.
  - BlueBird 757-200 (its own Wwise set, `bbs-757-200-base\sound`; the same on every variant): each engine at a node on its intake, at the fan, with a front layer (ConeHeading 0) and a rear layer (180) on the same node. The left and right electric hydraulic pumps sit in the wheel wells, under the wing views; the two centre pumps 4.2 m further back, closest to the behind-the-wing views; the flap motors between the two. The flaps, slats, gear drag and liftoff have no node, so they play at the datum, about 4 m ahead of the nose. The packs name nodes the model doesn't have. Most cabin ambience (packs, cabin wind, ground roll, passengers) plays from the cockpit door, aimed back down the cabin (ConeHeading 180). The sound.xml spells the engine and hydraulic nodes in lower case (`Soundnode_lengineintake`) where the model has `Soundnode_Lengineintake`. Whether the sim matches node names regardless of case wasn't verified; listen to Alt+1 against Alt+5 to check that each engine comes from its own side.

## 8a. Check the layout against real aircraft

The sound files say where each add-on plays a sound. Published measurements say where a real passenger hears it. Use both:

- **Fan and buzzsaw:** radiate forward out of the intake. Fan tones are strongest 20 to 40 degrees off the engine's forward axis and buzzsaw at 50 to 60; fan tones are about 14 dB weaker at 90 degrees, beside the engine (NASA TM X-71763, Heidmann). Boeing and Rolls-Royce measured buzzsaw in a 777's forward cabin.
- **Jet roar:** strongest 20 to 40 degrees off the exhaust axis, in the rear cabin: about rows 20 to 28 of a 180-seat A320 (DLR flight tests, AIAA 2013-2030). The add-ons here anchor the roar at the engine itself, so a view just behind the wing already sits in its rear sound.
- **Hydraulic pumps:** in or beside the main gear bay. That's the A320's green system and PTU (NTSB DCA12IA096), the 737's pump B in the right wheel well (FAA AD 99-26-21), and at least one 777 electric pump in the main gear wheel well (FAA). On the 757, Boeing's rescue chart puts hydraulic reservoirs in both main wheel wells (Boeing 757 ARFF chart); pilots' forums put the left and right electric pumps in their own wheel wells and the centre pumps in a bay behind the left one. That last part is secondary and wasn't confirmed from a Boeing document.
- **Window seats** measure about 4 dB louder than middle or aisle seats (A321 cabin, Canadian Acoustics 2006).
- **Check the model against the manufacturer's airport-planning documents** (Airbus Aircraft Characteristics, Boeing ACAPs). Here they agreed to about 0.1 m on the Fenix and 0.4 m on the PMDG and iFly models, for example the distance from the intake to the first overwing exit. On the BlueBird 757, doors 1 and 2 and the aft door are within 1 cm of Boeing's 757 ACAP (D6-58327 Rev H, p. 2-21), the engine centrelines within 5 cm, and the inlet lips within 0.2 m (RB211) and 0.25 m (PW2000).

## 9. Choose a target for each slot

**Starting targets (fore/aft positions are relative to the airframe features measured above)**

| View | Where | Heading from the nose | Pitch |
| --- | --- | --- | --- |
| Engine front | 50 to 60 degrees off the engine's forward axis, measured from the inlet lip and including the height difference. That is about 2.2 to 3.3 m ahead of the intake on a narrowbody and about 4.8 m on a 777. Sit 8 to 14 cm from the glass. | About 119 to 138 degrees, aimed between the lip and the fan | 21 to 28 degrees down |
| Over-wing | About 1 m behind the wing root's leading edge | 90 to 100 degrees | 14 degrees down |
| Wing | Over the flaps and main gear (mid-chord at the root) | 75 to 85 degrees | 13 degrees down |
| Behind the wing | 1.5 to 2.5 m behind the root trailing edge | 60 to 76 degrees | 12 degrees down |

Use these as starting points only: the search in step 11 picks the actual window, distance from the glass, heading and pitch.

Seat height is the window centre plus about 3 cm. Cabin zoom is 0.354. For Alt+9 keep the aircraft's existing pilot view. For Alt+0 put the camera 12 cm inside the front windshield found in step 7.

## 10. Check views offline with ray casting

Render each view as a small grid of rays (96 by 54 is plenty) through the assembled interior and exterior, and label what each ray hits first: sky, ground, airframe, engine, cabin, seat, cockpit, a back face, or a surface closer than 7 cm. Report, for the centre half of the frame:

- how much is outside (sky, ground, airframe, engine);
- how much is wing or engine, and engine alone;
- how much is "bad": rays hitting a back face or a surface closer than 7 cm. Either means the camera is inside something.

Rules that made the checker match the sim:

- Asobo and PMDG models use clockwise front faces. For interior geometry a back-face hit means the camera is inside it. For the exterior, cull back faces, because from inside, the view looks out through the hull.
- Glass, decals and invisible materials don't block. Window shades do if they are static and closed (PMDG 777-300ER, beside door 3).
- Exterior meshes that face into the cabin are walls, not airframe. The FlyByWire's `HublotIn` window lining was first counted as airframe, so blocked views scored "100% wing".
- Alpha-masked skins cut their window holes with a texture a ray-caster can't see (iFly `Max8_Fuselage*` and `Max8200_Fuselage*`). Treat them as see-through and let the side-wall panels behind them bound the view.
- Validate first. Before trusting the checker on an aircraft, run it on views known to work in the sim (existing views are ideal) and look at the rendered images. On the Fenix this caught three loader bugs before any file was written.

## 11. Search for the best seat

1. For each slot, take the 4 or 5 windows nearest the target and 4 or 5 distances in from the glass (10 to 45 cm on narrowbodies).
2. Score each candidate at low resolution: outside + 0.5 × wing/engine − 3 × bad − 12 × metres from the target − a small penalty per degree of heading change. For the engine-front view, weight the engine itself much more than general outside. Reject anything with more than 5% bad or a blocked centre.
3. Refine the best few with heading steps of 8 to 15 degrees and, for the engine view, a 6-degree pitch step.
4. Choose the engine-front window by angle, not by how much engine it shows. Take the line from the inlet lip to the camera, including the height difference, and measure its angle from the engine's forward axis. Pick a window at 50 to 60 degrees, then aim at the intake and require a clear view, with at least 10% engine in the middle of the frame. A score that rewards engine pixels pulls the seat back beside the intake, because the engine looks bigger there. Why 50 to 60: fan tones peak 20 to 40 degrees off the inlet axis and buzzsaw at 50 to 60, and both fade toward 90 (NASA TM X-71763). Further forward than about 50 degrees, a cabin window no longer shows the engine.
5. Leave the behind-the-wing view just behind the trailing edge. Real jet roar peaks a few rows further back, 20 to 40 degrees off the exhaust axis (DLR, AIAA 2013-2030). The add-ons checked here (Fenix, FlyByWire, iFly) anchor their engine sounds at the engine itself, at the fan or mid-nacelle, so moving the view back only adds distance.
6. Run one search per cabin layout. Engine-type and wingtip twins get the same views; spot-check a twin.
7. When the model is symmetric but the checker sees one side differently, mirror the good side. The FlyByWire's right wing faces the other way, so culling dropped it.
8. A full Fenix cabin is about 7 million triangles and 6 to 7 GB in Python. Run at most two searches next to a running sim.

## 12. Write the files

- Build the file with slots in the order 0, 9, 1, 2 ... 8, then any extra cameras the old file had (the Fenix A320 presets keep a camera titled "Pilot").
- Write with CRLF line endings and give each block a new Guid.
- Read every file back: block count, line endings, values.
- When fixing one view later, rewrite only that block's InitialXyz and InitialPbh and leave the rest byte-for-byte.
- Write the same views to every preset that shares the cabin: engine variants (Fenix CFM and IAE, 777 PW, GE and RR), wingtip variants (Fenix SL and WF, 737 BW and SSW), and a freighter that copies a passenger model. Then compare every slot across them.
- Keep the previous values of every moved view, as data, so a view can be put back if the old one is preferred.

## 12a. Name the seats (optional)

To describe each view as a passenger seat (for example 12A):

1. Load only the cabin's seat models: every class, including first-class seats with their own names, but not invisible click targets.
2. Take the vertices of window seats inboard of the cameras at upper seat-back height. Gather them from both sides of the cabin together, so a row counts once even where one side is missing a seat.
3. Group them along the cabin with a 15 cm gap rule. Each group is one row; number them from the front.
4. A camera belongs to the row whose seat back is just behind it. Left window seats are A. Right window seats are F on narrowbodies; on widebodies the right letter follows the seats abreast, skipping I.
5. Check the total row count against the cabin's seat count, and say plainly that real airline seat maps may skip row 13.

Freighters and VIP cabins have no numbered rows. An aircraft with no cabin model can borrow the rows of a sibling with the same airframe; the FlyByWire used the Fenix A320's.

## 13. Verify in the sim

1. Load the aircraft. Views are read only at load, so reload after any change.
2. Click the scenery through the windshield (not near the top edge, which opens the toolbar) so the sim has keyboard focus.
3. Press Alt+1 through Alt+0, waiting about 6 seconds after each for the camera to settle.
4. For each cabin view, check:
   - the window frame or reveal is around the edge;
   - the intended part is in view;
   - no wall, seat or lining blocks it.

   Night is fine for this.
5. Never press Ctrl+Alt+N while checking: it overwrites that slot with the current camera.
6. Check at least one aircraft per model family in the sim, plus any view that had to move (next to doors, unusual cabins).
7. To fine-tune a view by hand, load it, then use the cockpit camera keys. On this PC, Alt+Up and Alt+Down slide forward and back along the view direction, Left and Right slide sideways, and Shift+arrows turn the view. A tap moves a few centimetres or turns a few degrees, and the step varies, so count taps but trust the saved file. A camera facing the window moves toward the glass with Alt+Up. When it looks right, press Ctrl+Alt+N on purpose to save it, then read the file back. The sim rewrites the whole file with every slot it has loaded.
8. Lessons from hand-tuning:
   - **Raise the camera to see further down and back through a window.** To see further aft, move the eye forward, up and closer to the glass. Raising alone (Up arrow) was what worked on the 777 engine-front views.
   - **Alt+Up and Alt+Down follow the view's tilt.** With the camera looking down, Alt+Up also lowers it, which can hide the intended target.
   - **Slide steps aren't equal.** Repeated taps and single taps moved different amounts. If a move makes things worse, reload the view and repeat the sequence that worked, then save.
   - **Pressing the key of the active view returns to the cockpit.** To reload a view, press another view's key first.
   - **Ctrl+Alt+N writes only the loaded preset's file.** Copy the changed blocks to the sibling presets by hand, then compare every slot.
   - **Slides stop at cabin furniture.** The camera has a small collision radius, so a long move along the cabin can stall against a seat back. For a long move, start from the nearest view at the right point along the cabin, turn the camera to face the direction of travel, and level it. Then hold the slide key; about 0.85 m per second of hold was typical. Save and read the file after each step, then set the final angle last. A held look key turned about 74 degrees per second, and a single tap about 4 degrees.
   - **Overlays can swallow keys.** Pop-up add-on messages sometimes took a keypress, so a view didn't load or a save landed on the wrong camera. Confirm each step by reading the file back, not just by watching the screen.
   - **Reload after editing files while the aircraft is loaded.** Until the reload, the sim holds the old views in memory, and any save writes them back over the edited file.
9. Reloading without the menus: save the flight once over SimConnect (SimConnect_FlightSave), then load that .FLT (SimConnect_FlightLoad) after each change to the view files, and click "Ready to fly". The aircraft reloads and reads its view files again. The BlueBird 757 always comes back cold and dark.
10. Move the controls while checking, to see what each seat shows. Aircraft with their own systems may ignore the sim's default events. The BlueBird 757 put its flaps straight back after FLAPS_INCR; its levers are `L:B757_FC_FLAP_LEVER` (0 to 150; 41 is flaps 5, 150 is flaps 30) and `L:B757_FC_SPOILER_LEVER` (the speedbrake, 0 to 100), and they need hydraulic power. Its EFB's "Before start" preset gives that (battery, APU, AC power and the electric pumps in about 12 seconds); it can be pressed through the Coherent GT debugger (port 19999), as the msfs-blind-assist B757 branch does, more reliably than by clicking the tablet in 3D.

## 14. Pitfalls found on this project

**Symptom, cause and fix**

| Symptom | Cause | Fix |
| --- | --- | --- |
| Fenix window views showed no cabin wall | A skip filter containing "pane" also matched every "Wall_Panel" | Skip "window_pane" and glass explicitly, not "pane" |
| Fenix wing missing from renders | Wing XML used a LODS Template with MergeModel tips | Follow Template and MergeModel |
| Fuselage counted as engine | Its folder name (Function_Exterior_A320_CFM_SL) contained the engine type | Classify engines by part name (Part_Exterior_CFM / IAE) |
| Huge invisible planes and boxes in the cabin | Fenix rig helpers named `Skel_*` | Skip `Skel_*` |
| Window height 30 cm too high (iFly) | Measured from shades parked above the glass | Measure the glass in the interior model |
| Engine 1.7 m too far forward (iFly) | Ground safety cones in front of the engines | Skip cones, covers and chocks |
| Every iFly window looked solid | Fuselage skin with alpha-mask window holes | Treat masked Max8/Max8200 fuselage skins as see-through |
| FlyByWire views "100% wing" offline but blocked in the sim | Inward-facing window lining counted as airframe | Class it as a wall. Seat cameras in the gap between lining and hull (about 1.81 to 1.89 m out) |
| Right wing missing in FlyByWire renders | Its triangles face the other way, so culling dropped them | Mirror the left-side seats to the right |
| GoPro well behind the windshield | The mesh named like the windshield was the side window | Ray-cast straight ahead from the pilot's eye to find the front pane |
| 777-300ER over-wing views blocked | Static closed shades beside door 3 | Count shades as solid where they are modelled closed |
| A321 views moved off target | Doors 2 and 3 leave gaps in the window row | Accept the nearest window, then check those views in the sim |
| Engine-front views sat beside the intake instead of in front of it (777s, A320 family, iFly) | The seat search rewarded how much engine filled the frame, and the engine looks biggest from beside the intake | Choose the window by its angle to the inlet axis (50 to 60 degrees) first, then require a clear view |
| Engine-front view blank when moved forward, or showing the wall between two windows (PMDG 737, camera 30 cm in) | Looking 35 degrees or more aft through a small window, the window reveal hides the engine unless the camera is close to the glass | Sit 8 to 14 cm from the glass for these views and check that some engine is in the middle of the frame |
| 777-300ER views nudged toward the glass offline faced the wall in the sim | The sim placed the camera a little differently from the offline model (cause not found). Within a few centimetres of the wall, that decides the view | Make the last moves toward the glass by hand in the sim, then save with Ctrl+Alt+N |
| 757 eyepoint in the middle of the cabin, 26.5 m too far back, when the datum is taken as the model origin | Its datum is 86.82 ft ahead of the model origin (`reference_datum_position`), not at it | Add the datum offset to the eyepoint (step 5); check that the pack's own pilot camera lands over the captain's seat |
| 757 window centre 17 cm too low | The median of the panes' vertices, which bunch at each pane's lower edge | Take each pane's own centre (half way between its top and bottom), then the median of those |
| 757 first class counted as one row | Its seats are staggered 0.4 m across the aisle, so pooling both sides merged four rows into one | Find the rows on each side separately, then pair each with the row beside it across the aisle (centres within 0.6 m). A row with no partner counts once: the four-door cabin has a right-only row at door 2 |
| 757 flaps went back to 5 after a flap command | The aircraft runs its own flap lever and ignores the sim's FLAPS_INCR | Drive the aircraft's own lever variable (step 13.10) |

## 15. Aircraft notes from this project

**Eyepoints are in feet from the reference datum (longitudinal, lateral, vertical)**

| Aircraft | View file(s) | Eyepoint | Notes |
| --- | --- | --- | --- |
| PMDG 777-200ER, 777F | `PMDG 777-200ER / 777F \presets\pmdg\<preset>\config\cameras.CFG` | 82.122316, -1.74, 7.722 | 200ER tuned by hand in the sim. Its engine-front views were then moved ahead of door 2 and raised 6 cm by hand on the GE preset, then copied to PW, RR and the 777F. The 777F copies the 200ER. |
| PMDG 777-300ER | `PMDG 777-300ER\presets\pmdg\PMDG 777-300ER\config\cameras.CFG` | 99.559998, -1.74, 7.722 | Shades closed beside door 3. Alt+3/7 were finished by hand in the sim after an offline nudge toward the glass failed, and Alt+8 was moved by hand to mirror Alt+4. The engine-front views were moved 4.8 m ahead of the intake, then raised 4 cm by hand. |
| PMDG 737-700 / 800 / 900 | `PMDG 737-<type>\presets\pmdg\<preset>\config\cameras.CFG (29 presets)` | 37.312 / 47.075 / 52.139, -1.660, 3.909 | -700 cockpit attaches with offset 0,0,-3.0. Freighters have no cabin windows. The first build put the cabin cameras 30 cm in from the glass; the engine-front views need 8 cm. The BBJ's left side has no window in the 50 to 60 degree band. |
| Fenix A319 / A320 / A321 | `FNX_32X\presets\fnx\<preset>\config\cameras.cfg (20 presets)` | 38.650528 / 43.920738 / 57.965850, -1.623061, 3.955627 | Model origin is the datum. Parts span two packages. |
| FlyByWire A32NX | `FlyByWire_A320_NEO\cameras.CFG` | 43.72074, -1.723061, 4.355627 | No cabin model; windows painted on; HublotIn lining. The engines have SOUND_ENGINE nodes at the fan. |
| iFly 737 MAX 8 | `iFly 737-MAX8, -166Seats, -189Seats, -MAX8200 \cameras.CFG` | 49.683998, -1.63, 2.1 | Window glass at y about 0.47 and 1.82 m out. Its model.cfg says not to show the exterior in interior views, but the wing does show from the cabin in the sim, so load both models for checks. |
| PMDG 737-600 | `PMDG 737-600\presets\pmdg\PMDG 737-600 SC / TC\config\cameras.CFG` | Not measured here (the aircraft isn't installed on this PC) | Views by wolfman1360, who checked them in the sim. The cabin views are the 737-700 SC seats moved 1.37 m forward of the pilot with the wing, which matches the 54 in (1.37 m) Boeing removed ahead of the wing; SC and TC share one set of views. Alt+1 faces 146°, further back than on the other PMDG 737s. Seat numbers were worked out from the 737-700's measured rows. |
| TFDi MD-11, MD-11F | `TFDi_Design_MD-11\presets\tfdi-design\<preset>\config\cameras.CFG (8 presets)` | 69.0, -2.20, 1.4 | Views by wolfman1360. One model per preset, with the engines merged in by MergeModel; model origin is the datum. The eyepoint sits 4.7 m behind the pilot's camera. The freighter has two cabin windows per side, used by Alt+2/3/6/7; the other cabin views have no window and are for sound only. Checked offline against the MD-11F model (ray cast, GoPro 12.4 cm inside the windshield). The passenger presets copy the freighter's file; the passenger cabin isn't installed here. |
| BlueBird 757-200 | `bbs-757-200-<variant>\cameras.CFG (10 variants)` | -20.66667, -2, 4.6, from a datum 86.81667 ft ahead of the model origin | One model per variant folder, like the iFly; sound and behaviours come from `bbs-757-200-base`. Liveries are separate folders that point at a variant (`base_container`) and use its view file. The pack's own pilot camera is 0.08 m behind and 0.22 m above the eyepoint. Window panes (`Cabin_innerGLASS`) at 1.847 m out, centres at y 1.605 m, 0.51 m apart; door 2 covers most of the 50 to 60 degree engine-front band, so Alt+1/5 use the first window ahead of it (46 and 49 degrees off the inlet axis on the RR, 48 and 51 on the PW, whose inlet lip is 0.28 m further forward). Three searches (RR without winglets, RR four-door, PW); the four-door came out within 0.1 mm of the standard cabin, so the PW four-door versions copy the PW set, and the winglet and no-cabin versions copy their twin. Checked in the sim: all ten views on the RR without winglets, with the flaps (30) and speedbrake moved; three to five views each on the RR four-door, the PW and the PW with no cabin, which keeps the window reveals. |

## 16. The reference scripts

The folder `Reference scripts` holds the Python used here, as it ran. Paths point at this PC's install (`D:\MSFS2024 Community\Community` and the Steam user folder), so adjust them first. See `README.txt` in that folder for what each does.
