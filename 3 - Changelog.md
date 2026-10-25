# Changelog

This is what changed after the first version of these views, and why. The newest change is first.

## Added: BlueBird 757-200 (25 October 2026)

Views for the BlueBird Simulations 757-200 were added: one file for each of its ten versions, so the set now has 79 view files. They use the same ten keys as every other aircraft.

- **Checked in the sim:** all ten views on the Rolls-Royce version without winglets, with the flaps run out to 30 and the speedbrake raised, and three to five views each on the Rolls-Royce four-door, the Pratt & Whitney and the Pratt & Whitney with no cabin.
- **Versions:** Pratt & Whitney and Rolls-Royce engines, with and without winglets, the Rolls-Royce with split scimitar winglets, the four-door cabins ("AWE"), and the Pratt & Whitney with no cabin. The wingtip doesn't change any seat. The four-door cabin's third door is further back than any view, so it uses the same seats as the standard cabin; only its row numbers differ.
- **Engine-front views:** on the 757 the usual angle in front of the engine falls mostly on door 2, so these views use the first window ahead of it, 46 to 51° off the engine's axis, looking back into the intake.
- **Where the sounds are:** each engine plays from its intake, with separate front and rear sounds. The electric hydraulic pumps play from the wheel wells, under the wing views. BlueBird's flaps, slats and gear sounds have no position, so they play from the aircraft's reference point, which on this aircraft is about 4 m ahead of the nose.
- **Checked against Boeing's 757 airport-planning document:** BlueBird's doors match it to 1 cm and the engines to 0.25 m.
- Documents: a new section in [1 - What each view is.md](1%20-%20What%20each%20view%20is.md), and the 757's sound sources, frame of reference and pitfalls in [2 - How to build sound views from scratch.md](2%20-%20How%20to%20build%20sound%20views%20from%20scratch.md). The script that built them is `Reference scripts\gen757.py`.

## Guides are now Markdown

The three guides were converted from HTML pages to Markdown (`.md`) files, so GitHub shows them as formatted pages. In the download they open in any text editor. Their content didn't change.

## Added: PMDG 737-600 and TFDi MD-11

wolfman1360 made views for two more aircraft, and they were added to the set, which now has 69 view files. They use the same ten keys as every other aircraft.

- **PMDG 737-600** (SC and TC cabins): checked in the sim by wolfman1360. The views over, on and behind the wing use the same seats as the 737-700, moved forward with the shorter cabin. The left engine-front view (Alt+1) looks further back toward the engine than on the other 737s. The 737-600 isn't installed on the PC these documents were written on, so its seat numbers were worked out from the 737-700's cabin.
- **TFDi MD-11F** (GE and PW engines, with and without the LOW option): checked against TFDi's own 3D model, not yet in the sim. The engine-front views sit 4.5 m ahead of the engine, the GoPro sits 12 cm inside the windshield, and the pilot seat is TFDi's own pilot view. The freighter has only two windows on each side. The over-the-wing and wing views use them; the engine-front and behind-the-wing views face the cargo-deck wall and are for sound only.
- **TFDi MD-11** (passenger, same four presets): uses the freighter's views, as it's the same airframe. Not checked, because the passenger cabin isn't installed here. TFDi doesn't publish its seat map, so these seats are described by the nearest door instead of a row number.
- The MD-11 has a third engine in the tail. Its sound plays from the tail, more than 20 m behind every cabin view; the closest are the behind-the-wing views, Alt+4 and Alt+8.
- Documents: new sections for both aircraft in [1 - What each view is.md](1%20-%20What%20each%20view%20is.md), and their sound sources and notes in [2 - How to build sound views from scratch.md](2%20-%20How%20to%20build%20sound%20views%20from%20scratch.md).

## In short

- The engine-front views (Alt+1 and Alt+5) were moved on every aircraft so they now sit properly in front of the engine.
- All the other views were reviewed and stayed where they were. They were already in the right spots.
- The new views were checked in the sim on every aircraft except the A319 and the 777F, which use the same seats as aircraft that were checked.
- The documents were updated to match.

## Why the engine-front views moved

The engine-front view is meant to put the listener a few rows ahead of the engine, looking back into the intake. That's where the fan whine and the "buzzsaw" sound on takeoff come through best.

In the first version, most of these views ended up too far back. On the 777s, the Fenix A319, A320 and A321, the FlyByWire A32NX and the iFly 737 MAX 8, the seat was almost beside the intake instead of in front of it. The program that picked the seats preferred windows where the engine looked biggest, and the engine looks biggest from right beside it.

The PMDG 737s had a different problem. Their seats were in the right place along the cabin, but the camera sat 30 cm back from the window. From there the view showed mostly the wall between two windows, and the engine only appeared in the next window back.

All of these views now sit a few rows in front of the engine, right up against the window, looking back into the intake.

## What changed on each aircraft

Seat numbers are for the left side. The right side uses the matching seat across the aisle.

**Engine-front views (Alt+1 and Alt+5), before and after**

| Aircraft | Before | Now | Seat |
| --- | --- | --- | --- |
| Fenix A320 | 1.4 m in front of the engine | 3 m in front of the engine | 6A, now 4A |
| Fenix A319 | Same as the A320 | Same as the A320 | 4A, now 2A |
| Fenix A321 | Level with the engine | 3 m in front, at the window just ahead of door 2 | Single-class 11A, now 10A; two-class 8A, now 7A |
| FlyByWire A32NX | 0.6 m in front of the engine | 3.3 m in front of the engine | 7A, now 3A |
| PMDG 777-200ER (PW, GE and RR) | Level with the engine | 4.8 m in front, at the window just ahead of door 2 | 14A, now 10A |
| PMDG 777-300ER | Level with the engine | 4.8 m in front of the engine | 17A, now 13A |
| PMDG 777F | Level with the engine | Same as the 777-200ER | No seats (cargo deck) |
| iFly 737 MAX 8 | 1 m in front of the engine | 2.7 m in front of the engine | 189-seat 9A, now 7A; 178-seat 8A, now 5A; 166-seat 7A, now 5A; MAX 8200 8A, now 6A |
| PMDG 737-800 | 3.1 m in front, but 30 cm back from the window | 2.6 m in front, right up against the window | Single-class 6A, now 7A; two-class 5A, now 6A |
| PMDG 737-900 and 900ER | 3.1 m in front, but 30 cm back from the window | 2.6 m in front, right up against the window | 900ER single-class 8A, now 9A; 900 two-class 7A, now 8A |
| PMDG 737-700 | 3.2 to 3.8 m in front, 15 to 30 cm back from the window | 2.2 to 2.7 m in front, right up against the window | Single-class 1A, now 3A; two-class 2A, now 3A |

On the 737s the seat number goes up by a row or two. The new seat is a window or two further back, but because it's right at the glass, the engine is finally in view.

A few notes:

- Every version of each aircraft got the same change. That includes the Fenix CFM and IAE engines and both wingtips, the 777 engine options, and the 737's blended and split scimitar winglets.
- The 737 BBJ's left side has no window far enough forward, so its Alt+1 uses the furthest-forward window it has.
- The 737 freighters and the 777F have no cabin windows. The 737 freighters were left alone, and the 777F simply copies the 777-200ER for sound.

## Fine-tuning in the sim

On the two 777s the engine sat right at the edge of what the window shows. Both engine-front views were raised slightly by hand in the sim, 4 cm on the 777-300ER and 6 cm on the 777-200ER, so more of the intake and fan shows. The 777-200ER change was then copied to its other two engine versions and to the 777F.

On the 777-300ER, the right behind-the-wing view (Alt+8) showed mostly ground, with only a thin strip of wing. It was moved one window forward and tilted a little further down, so it now mirrors the left one (Alt+4). With the flaps out, both now show the flaps and the whole wing from behind. The seat stays 38K.

## What stayed the same, and why

- **Over the wing (Alt+2/6):** these were already the closest seats to the slats, the flap motor, the air conditioning and, on the Airbuses, the "barking dog" hydraulic pump.
- **Wing (Alt+3/7):** these were already over the flaps and the main landing gear, where real airliners keep their hydraulic pumps. On the 737 the hydraulic pump sounds play right below these seats. On the 777 they sit next to where the hydraulic whine was found loudest by ear.
- **Behind the wing (Alt+4/8):** these were already well inside each engine's rear sound. In a real aircraft the jet roar is loudest a few rows further back, but these add-ons play the roar from the engine itself, so moving back would mostly just make it quieter.
- **Pilot seat and windshield (Alt+9 and Alt+0):** unchanged.

## What to expect when listening

- From the new engine-front seats the engine may sound a little quieter, because the seat is further from where the sound is played. It also arrives from behind and to the side, as it would on a real flight.
- For the loudest engine sound, use the over-wing views, Alt+2 and Alt+6.
- The old positions were kept on file, so any aircraft can be put back the way it was.

## What the research found

The review was based on published measurements and on each aircraft's own sound files:

- **Fan whine and buzzsaw** come out of the front of the engine. They're loudest at an angle in front of it and much weaker straight out to the side. Sources: NASA's fan-noise method (Heidmann, NASA TM X-71763), and Boeing and Rolls-Royce measurements of buzzsaw in a 777's forward cabin.
- **Jet roar** is loudest behind the wing, in the rear cabin: around rows 20 to 28 on a 180-seat A320 (DLR flight tests, AIAA 2013-2030).
- **Window seats** are about 4 dB louder than middle and aisle seats (A321 cabin measurements, Canadian Acoustics, 2006).
- **Hydraulic pumps** sit in or next to the main landing gear bay on the A320, 737 and 777 (NTSB report DCA12IA096, FAA AD 99-26-21 and an FAA 777 pump directive).
- **The 3D models are accurate.** They match Airbus's and Boeing's own airport-planning documents to within 0.1 to 0.4 m.
- **Passenger seat maps** put the classic "engine view" a few rows ahead of the intake, which matches the new seats. These are traveller reports, not measurements.
- **Each aircraft's sound files** show where its sounds actually play from:
  - The Fenix plays each engine from a single point in the middle of the engine.
  - The FlyByWire and the iFly play each engine from its fan, with separate front and rear sounds.
  - The iFly's hydraulic and flap sounds play from the middle of the aircraft, over the wing.
  - The 737 sound pack plays its hydraulic pumps right under the wing views.

## Other updates

- **What each view is:** clearer descriptions, a new "Why these seats" section, and the new seat numbers.
- **How to build sound views from scratch:**
  - the new rule for placing the engine-front view;
  - how to measure the engine;
  - where each aircraft plays its sounds;
  - a new section on checking the layout against real aircraft;
  - tips for fine-tuning views by hand;
  - more pitfalls to avoid.
- **Seat numbers:** a small fix in how seats across the cabin are counted. It had briefly mislabelled the 777-300ER's right window seats.
- **Reference scripts:** new tools for the engine-front search, for choosing and writing the new seats, and for reading where an aircraft plays its sounds.

## One more change, made just before the review

On the 777-300ER, the wing views (Alt+3 and Alt+7) were moved 16 to 20 cm closer to their windows and turned toward the glass, so more of the wing shows. They're now listed as seats 33A and 33K instead of 34A and 34K.
