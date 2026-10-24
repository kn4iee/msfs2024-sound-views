# What each view is

These are custom cabin camera views for Microsoft Flight Simulator 2024, picked for how they sound rather than how they look. In the sim the camera is also the listener, so each view is a window seat placed next to a part of the aircraft that makes an interesting noise. The set has 69 view files. [3 - Changelog.md](3%20-%20Changelog.md) explains what changed since the first version.

## The ten views

The keys do the same thing on every aircraft.

**What each key shows and hears**

| Key | View | What it's for |
| --- | --- | --- |
| Alt+1 (left), Alt+5 (right) | Engine front | A window seat a few rows ahead of the engine, looking back into the intake. Best for the fan whine and the "buzzsaw" sound on takeoff. |
| Alt+2 (left), Alt+6 (right) | Over the wing | Right above the front of the wing, beside the engine. The loudest seat for the engine, with the slats and air conditioning close by. |
| Alt+3 (left), Alt+7 (right) | Wing | Over the middle and back of the wing. The flaps, the main landing gear and the hydraulic pumps. |
| Alt+4 (left), Alt+8 (right) | Behind the wing | Just behind the wing, looking forward at it. Engine roar and flap noise, and a good view of the wing on approach. |
| Alt+9 | Pilot seat | The aircraft's normal pilot view. |
| Alt+0 | Windshield GoPro | Just inside the captain's windshield, looking ahead. The best view for watching an approach. |

## Why these seats

Each seat was checked against published measurements and against where each aircraft actually plays its sounds.

- **Engine front:** the fan whine and buzzsaw come out of the front of the engine. They're loudest at an angle in front of it and much weaker straight out to the side (NASA's fan-noise method, Heidmann, NASA TM X-71763). Boeing and Rolls-Royce measured buzzsaw in a 777's forward cabin. That's why these seats sit a few rows ahead of the engine rather than beside it.
- **Over the wing:** the drive for the slats and flaps sits in the middle of the aircraft. These are the nearest windows to where each aircraft plays the slats, flap motor and air conditioning. On the Airbuses and the iFly, the hydraulic pump sounds play here too.
- **Wing:** real airliners keep their hydraulic pumps in or next to the main landing gear bay. That's true of the A320, the 737 and the 777 (NTSB report DCA12IA096, FAA AD 99-26-21 and an FAA 777 pump directive). These seats sit right above that area and the flaps.
- **Behind the wing:** in a real cabin the jet roar is loudest a few rows further back, around rows 20 to 28 on an A320 (DLR flight tests, AIAA 2013-2030). These aircraft play the roar from the engine itself, so a seat just behind the wing already gets it. Moving further back would mostly just make it quieter.
- **Window seats:** every cabin view is at the window, because window seats are about 4 dB louder than middle or aisle seats (A321 cabin measurements, Canadian Acoustics, 2006).

## Installing

1. Close the aircraft first, or stay at the sim's main menu. Views are only read when an aircraft loads.
2. Copy the folders inside `Views` into the sim's `SimObjects\Airplanes` user folder, and let Windows merge the folders and replace the files. For the Steam version of the sim that folder is `%APPDATA%\Microsoft Flight Simulator 2024\SimObjects\Airplanes`.
3. This replaces any custom views already saved on those keys. To keep the old ones, copy their files somewhere safe first.
4. Load the aircraft and press Alt+1 through Alt+0. Each view takes about 6 seconds to settle.
5. Avoid pressing Ctrl+Alt with a number unless saving on purpose. That saves the current camera over that key's view.

## Each aircraft's views

How to read the tables:

- **Where it sits:** the distance back from the pilot's seat, and out from the middle of the aircraft.
- **Facing:** measured from the nose. 90° looks straight out of the window; more than 90° looks back toward the tail.
- **Seat:** counted from the front row of the sim's cabin. A is the left window seat. The right window seat is F on the narrowbodies and K on the 777s. Real airlines often skip row 13 or number their seats differently, so a real ticket may be a row or two off. TFDi doesn't publish the passenger MD-11's seat map, so its Seat column gives the distance from the nearest door instead.

Jump to an aircraft:

- [PMDG 777-200ER](#pmdg-777-200er)
- [PMDG 777-300ER](#pmdg-777-300er)
- [PMDG 777F](#pmdg-777f)
- [PMDG 737-600](#pmdg-737-600)
- [PMDG 737-700](#pmdg-737-700)
- [PMDG 737-800](#pmdg-737-800)
- [PMDG 737-900](#pmdg-737-900)
- [Fenix A319](#fenix-a319)
- [Fenix A320](#fenix-a320)
- [Fenix A321](#fenix-a321)
- [FlyByWire A32NX](#flybywire-a32nx)
- [iFly 737 MAX 8](#ifly-737-max-8)
- [TFDi MD-11F](#tfdi-md-11f)
- [TFDi MD-11](#tfdi-md-11)

## PMDG 777-200ER

**Status:** Fine-tuned in the sim and identical on the PW, GE and RR versions. The engine-front views sit at the window just ahead of door 2, raised slightly by hand so more of the intake shows.

**Sound:** Boris Audio Works sound pack. Its engines have separate front and rear sounds, which the engine-front and behind-the-wing seats pick up. The hydraulic whine is loudest just behind Alt+3/7, one seat in from the window.

**Applies to: PMDG 777-200ER GE, PMDG 777-200ER PW, PMDG 777-200ER RR**

| Key | View | Seat | Where it sits | Facing |
| --- | --- | --- | --- | --- |
| Alt+1 | Engine front (left) | 10A | 13.3 m behind the pilot, 2.91 m out from the centreline | 119° left of the nose, 21° down |
| Alt+2 | Over the wing (left) | 21A | 25.1 m behind the pilot, 2.50 m out from the centreline | 90° left of the nose, 14° down |
| Alt+3 | Wing (left) | 29A | 32.6 m behind the pilot, 2.68 m out from the centreline | 62° left of the nose, 14° down |
| Alt+4 | Behind the wing (left) | 32A | 36.3 m behind the pilot, 2.57 m out from the centreline | 69° left of the nose, 14° down |
| Alt+5 | Engine front (right) | 10K | 13.3 m behind the pilot, 2.91 m out from the centreline | 119° right of the nose, 21° down |
| Alt+6 | Over the wing (right) | 21K | 25.1 m behind the pilot, 2.60 m out from the centreline | 93° right of the nose, 13° down |
| Alt+7 | Wing (right) | 29K | 32.6 m behind the pilot, 2.66 m out from the centreline | 62° right of the nose, 12° down |
| Alt+8 | Behind the wing (right) | 32K | 36.3 m behind the pilot, 2.55 m out from the centreline | 63° right of the nose, 12° down |
| Alt+9 | Pilot seat | Captain's seat | The pilot's seat | straight ahead, 13° down |
| Alt+0 | Windshield GoPro | Cockpit, at the windshield | 0.40 m ahead of the pilot's eye, 0.29 m left of centre | straight ahead, 8° down |

## PMDG 777-300ER

**Status:** Checked in the sim. The views over the wing (Alt+2/6) were moved to avoid closed window shades beside door 3. The wing views (Alt+3/7) were moved closer to their windows by hand so more of the wing shows, and the right behind-the-wing view (Alt+8) was moved to mirror the left one (Alt+4), so both show the flaps from behind. The engine-front views sit a few rows ahead of the engines and were raised slightly by hand.

**Sound:** Same Boris Audio Works sound pack as the 777-200ER.

**File: PMDG 777-300ER**

| Key | View | Seat | Where it sits | Facing |
| --- | --- | --- | --- | --- |
| Alt+1 | Engine front (left) | 13A | 18.1 m behind the pilot, 2.90 m out from the centreline | 119° left of the nose, 21° down |
| Alt+2 | Over the wing (left) | 24A (extra legroom / exit area) | 28.3 m behind the pilot, 2.83 m out from the centreline | 90° left of the nose, 14° down |
| Alt+3 | Wing (left) | 33A | 37.9 m behind the pilot, 2.84 m out from the centreline | 79° left of the nose, 13° down |
| Alt+4 | Behind the wing (left) | 38A | 41.1 m behind the pilot, 2.83 m out from the centreline | 69° left of the nose, 14° down |
| Alt+5 | Engine front (right) | 13K | 18.1 m behind the pilot, 2.90 m out from the centreline | 119° right of the nose, 21° down |
| Alt+6 | Over the wing (right) | 24K (extra legroom / exit area) | 28.3 m behind the pilot, 2.83 m out from the centreline | 93° right of the nose, 13° down |
| Alt+7 | Wing (right) | 33K | 37.9 m behind the pilot, 2.81 m out from the centreline | 80° right of the nose, 11° down |
| Alt+8 | Behind the wing (right) | 38K | 41.1 m behind the pilot, 2.84 m out from the centreline | 70° right of the nose, 14° down |
| Alt+9 | Pilot seat | Captain's seat | The pilot's seat | straight ahead, 13° down |
| Alt+0 | Windshield GoPro | Cockpit, at the windshield | 0.40 m ahead of the pilot's eye, 0.29 m left of centre | straight ahead, 8° down |

## PMDG 777F

**Status:** Uses the same seats as the 777-200ER. The freighter's main deck has no windows, so these views are for sound only. Not checked in the sim.

**Sound:** Same Boris Audio Works sound pack as the 777-200ER.

**File: PMDG 777F**

| Key | View | Seat | Where it sits | Facing |
| --- | --- | --- | --- | --- |
| Alt+1 | Engine front (left) | no seats (cargo deck) | 13.3 m behind the pilot, 2.91 m out from the centreline | 119° left of the nose, 21° down |
| Alt+2 | Over the wing (left) | no seats (cargo deck) | 25.1 m behind the pilot, 2.50 m out from the centreline | 90° left of the nose, 14° down |
| Alt+3 | Wing (left) | no seats (cargo deck) | 32.6 m behind the pilot, 2.68 m out from the centreline | 62° left of the nose, 14° down |
| Alt+4 | Behind the wing (left) | no seats (cargo deck) | 36.3 m behind the pilot, 2.57 m out from the centreline | 69° left of the nose, 14° down |
| Alt+5 | Engine front (right) | no seats (cargo deck) | 13.3 m behind the pilot, 2.91 m out from the centreline | 119° right of the nose, 21° down |
| Alt+6 | Over the wing (right) | no seats (cargo deck) | 25.1 m behind the pilot, 2.60 m out from the centreline | 93° right of the nose, 13° down |
| Alt+7 | Wing (right) | no seats (cargo deck) | 32.6 m behind the pilot, 2.66 m out from the centreline | 62° right of the nose, 12° down |
| Alt+8 | Behind the wing (right) | no seats (cargo deck) | 36.3 m behind the pilot, 2.55 m out from the centreline | 63° right of the nose, 12° down |
| Alt+9 | Pilot seat | Captain's seat | The pilot's seat | straight ahead, 13° down |
| Alt+0 | Windshield GoPro | Cockpit, at the windshield | 0.40 m ahead of the pilot's eye, 0.29 m left of centre | straight ahead, 8° down |

## PMDG 737-600

**Status:** Views by wolfman1360, who checked them in the sim. The views over, on and behind the wing use the same seats as the 737-700, moved 1.37 m forward with the shorter cabin, which is how much shorter Boeing made the 737-600 ahead of the wing. The single-class and two-class cabins share one set of views; in the two-class cabin both engine-front views are in first class. The left engine-front view (Alt+1) faces 146°, further back than on the other 737s. The 737-600 isn't installed on the PC these notes were written on, so its seat numbers were worked out from the 737-700's cabin and may be a row off.

**Sound:** Same Boris Audio Works sound pack as the 737-700, with the same sound files.

### Set 1 of 2

**Applies to: PMDG 737-600 SC**

| Key | View | Seat | Where it sits | Facing |
| --- | --- | --- | --- | --- |
| Alt+1 | Engine front (left) | 1A | 3.6 m behind the pilot, 1.77 m out from the centreline | 146° left of the nose, 27° down |
| Alt+2 | Over the wing (left) | 8A | 9.3 m behind the pilot, 1.55 m out from the centreline | 92° left of the nose, 14° down |
| Alt+3 | Wing (left) | 11A | 12.5 m behind the pilot, 1.70 m out from the centreline | 72° left of the nose, 13° down |
| Alt+4 | Behind the wing (left) | 15A | 15.6 m behind the pilot, 1.70 m out from the centreline | 75° left of the nose, 12° down |
| Alt+5 | Engine front (right) | 1F | 4.1 m behind the pilot, 1.77 m out from the centreline | 135° right of the nose, 24° down |
| Alt+6 | Over the wing (right) | 8F | 9.3 m behind the pilot, 1.55 m out from the centreline | 92° right of the nose, 14° down |
| Alt+7 | Wing (right) | 11F | 12.5 m behind the pilot, 1.70 m out from the centreline | 72° right of the nose, 13° down |
| Alt+8 | Behind the wing (right) | 15F | 15.6 m behind the pilot, 1.70 m out from the centreline | 75° right of the nose, 12° down |
| Alt+9 | Pilot seat | Captain's seat | The pilot's seat | straight ahead, 11° down |
| Alt+0 | Windshield GoPro | Cockpit, at the windshield | 0.54 m ahead of the pilot's eye, 0.25 m left of centre | straight ahead, 8° down |

### Set 2 of 2

**Applies to: PMDG 737-600 TC**

| Key | View | Seat | Where it sits | Facing |
| --- | --- | --- | --- | --- |
| Alt+1 | Engine front (left) | 1A | 3.6 m behind the pilot, 1.77 m out from the centreline | 146° left of the nose, 27° down |
| Alt+2 | Over the wing (left) | 7A | 9.3 m behind the pilot, 1.55 m out from the centreline | 92° left of the nose, 14° down |
| Alt+3 | Wing (left) | 10A | 12.5 m behind the pilot, 1.70 m out from the centreline | 72° left of the nose, 13° down |
| Alt+4 | Behind the wing (left) | 15A | 15.6 m behind the pilot, 1.70 m out from the centreline | 75° left of the nose, 12° down |
| Alt+5 | Engine front (right) | 2F | 4.1 m behind the pilot, 1.77 m out from the centreline | 135° right of the nose, 24° down |
| Alt+6 | Over the wing (right) | 7F | 9.3 m behind the pilot, 1.55 m out from the centreline | 92° right of the nose, 14° down |
| Alt+7 | Wing (right) | 10F | 12.5 m behind the pilot, 1.70 m out from the centreline | 72° right of the nose, 13° down |
| Alt+8 | Behind the wing (right) | 15F | 15.6 m behind the pilot, 1.70 m out from the centreline | 75° right of the nose, 12° down |
| Alt+9 | Pilot seat | Captain's seat | The pilot's seat | straight ahead, 11° down |
| Alt+0 | Windshield GoPro | Cockpit, at the windshield | 0.54 m ahead of the pilot's eye, 0.25 m left of centre | straight ahead, 8° down |

## PMDG 737-700

**Status:** Checked in the sim. The engine-front views sit right up against the window, a few rows ahead of the engine. The BBJ's left side has no window far enough forward, so its Alt+1 uses the furthest-forward window it has.

**Sound:** Boris Audio Works 737NG sound pack. Its hydraulic pump sounds play right below Alt+3/7, and the flap motor plays from the middle of the aircraft, nearest Alt+2/6.

### Set 1 of 4

**Applies to: PMDG 737-700 BW SC, PMDG 737-700 SSW SC**

| Key | View | Seat | Where it sits | Facing |
| --- | --- | --- | --- | --- |
| Alt+1 | Engine front (left) | 3A | 5.1 m behind the pilot, 1.77 m out from the centreline | 123° left of the nose, 28° down |
| Alt+2 | Over the wing (left) | 9A | 10.7 m behind the pilot, 1.55 m out from the centreline | 92° left of the nose, 14° down |
| Alt+3 | Wing (left) | 13A | 13.9 m behind the pilot, 1.70 m out from the centreline | 72° left of the nose, 13° down |
| Alt+4 | Behind the wing (left) | 17A | 17.0 m behind the pilot, 1.70 m out from the centreline | 75° left of the nose, 12° down |
| Alt+5 | Engine front (right) | 3F | 5.6 m behind the pilot, 1.77 m out from the centreline | 122° right of the nose, 25° down |
| Alt+6 | Over the wing (right) | 9F | 10.7 m behind the pilot, 1.55 m out from the centreline | 92° right of the nose, 14° down |
| Alt+7 | Wing (right) | 13F | 13.9 m behind the pilot, 1.70 m out from the centreline | 72° right of the nose, 13° down |
| Alt+8 | Behind the wing (right) | 17F | 17.0 m behind the pilot, 1.70 m out from the centreline | 75° right of the nose, 12° down |
| Alt+9 | Pilot seat | Captain's seat | The pilot's seat | straight ahead, 11° down |
| Alt+0 | Windshield GoPro | Cockpit, at the windshield | 0.54 m ahead of the pilot's eye, 0.25 m left of centre | straight ahead, 8° down |

### Set 2 of 4

**Applies to: PMDG 737-700 BW TC, PMDG 737-700 SSW TC**

| Key | View | Seat | Where it sits | Facing |
| --- | --- | --- | --- | --- |
| Alt+1 | Engine front (left) | 3A (extra legroom / exit area) | 5.1 m behind the pilot, 1.77 m out from the centreline | 123° left of the nose, 28° down |
| Alt+2 | Over the wing (left) | 9A | 10.7 m behind the pilot, 1.55 m out from the centreline | 92° left of the nose, 14° down |
| Alt+3 | Wing (left) | 12A | 13.9 m behind the pilot, 1.55 m out from the centreline | 62° left of the nose, 13° down |
| Alt+4 | Behind the wing (left) | 17A | 17.0 m behind the pilot, 1.55 m out from the centreline | 65° left of the nose, 12° down |
| Alt+5 | Engine front (right) | 3F | 5.6 m behind the pilot, 1.77 m out from the centreline | 122° right of the nose, 25° down |
| Alt+6 | Over the wing (right) | 9F | 10.7 m behind the pilot, 1.55 m out from the centreline | 92° right of the nose, 14° down |
| Alt+7 | Wing (right) | 12F | 13.9 m behind the pilot, 1.55 m out from the centreline | 62° right of the nose, 13° down |
| Alt+8 | Behind the wing (right) | 17F | 17.0 m behind the pilot, 1.55 m out from the centreline | 65° right of the nose, 12° down |
| Alt+9 | Pilot seat | Captain's seat | The pilot's seat | straight ahead, 11° down |
| Alt+0 | Windshield GoPro | Cockpit, at the windshield | 0.54 m ahead of the pilot's eye, 0.25 m left of centre | straight ahead, 8° down |

### Set 3 of 4

**Applies to: PMDG 737-700BDSF BW**

| Key | View | Seat | Where it sits | Facing |
| --- | --- | --- | --- | --- |
| Alt+1 | Engine front (left) | no seats (cargo deck) | 4.6 m behind the pilot, 1.55 m out from the centreline | 120° left of the nose, 20° down |
| Alt+2 | Over the wing (left) | no seats (cargo deck) | 10.9 m behind the pilot, 1.40 m out from the centreline | 92° left of the nose, 14° down |
| Alt+3 | Wing (left) | no seats (cargo deck) | 15.0 m behind the pilot, 1.10 m out from the centreline | 62° left of the nose, 13° down |
| Alt+4 | Behind the wing (left) | no seats (cargo deck) | 17.4 m behind the pilot, 1.10 m out from the centreline | 65° left of the nose, 12° down |
| Alt+5 | Engine front (right) | no seats (cargo deck) | 4.5 m behind the pilot, 1.55 m out from the centreline | 120° right of the nose, 20° down |
| Alt+6 | Over the wing (right) | no seats (cargo deck) | 10.9 m behind the pilot, 1.55 m out from the centreline | 92° right of the nose, 14° down |
| Alt+7 | Wing (right) | no seats (cargo deck) | 15.0 m behind the pilot, 1.55 m out from the centreline | 62° right of the nose, 13° down |
| Alt+8 | Behind the wing (right) | no seats (cargo deck) | 17.4 m behind the pilot, 1.55 m out from the centreline | 65° right of the nose, 12° down |
| Alt+9 | Pilot seat | Captain's seat | The pilot's seat | straight ahead, 11° down |
| Alt+0 | Windshield GoPro | Cockpit, at the windshield | 0.54 m ahead of the pilot's eye, 0.25 m left of centre | straight ahead, 8° down |

### Set 4 of 4

**Applies to: PMDG 737-BBJ BW, PMDG 737-BBJ SSW**

| Key | View | Seat | Where it sits | Facing |
| --- | --- | --- | --- | --- |
| Alt+1 | Engine front (left) | VIP cabin (no numbered rows) | 6.1 m behind the pilot, 1.77 m out from the centreline | 116° left of the nose, 27° down |
| Alt+2 | Over the wing (left) | VIP cabin (no numbered rows) | 10.7 m behind the pilot, 1.55 m out from the centreline | 92° left of the nose, 14° down |
| Alt+3 | Wing (left) | VIP cabin (no numbered rows) | 13.9 m behind the pilot, 1.55 m out from the centreline | 62° left of the nose, 13° down |
| Alt+4 | Behind the wing (left) | VIP cabin (no numbered rows) | 17.0 m behind the pilot, 1.55 m out from the centreline | 65° left of the nose, 12° down |
| Alt+5 | Engine front (right) | VIP cabin (no numbered rows) | 5.6 m behind the pilot, 1.77 m out from the centreline | 117° right of the nose, 30° down |
| Alt+6 | Over the wing (right) | VIP cabin (no numbered rows) | 10.7 m behind the pilot, 1.55 m out from the centreline | 92° right of the nose, 14° down |
| Alt+7 | Wing (right) | VIP cabin (no numbered rows) | 13.4 m behind the pilot, 1.70 m out from the centreline | 72° right of the nose, 13° down |
| Alt+8 | Behind the wing (right) | VIP cabin (no numbered rows) | 17.0 m behind the pilot, 1.55 m out from the centreline | 65° right of the nose, 12° down |
| Alt+9 | Pilot seat | Captain's seat | The pilot's seat | straight ahead, 11° down |
| Alt+0 | Windshield GoPro | Cockpit, at the windshield | 0.54 m ahead of the pilot's eye, 0.25 m left of centre | straight ahead, 8° down |

## PMDG 737-800

**Status:** Checked in the sim. The engine-front views sit right up against the window, a few rows ahead of the engine.

**Sound:** Same Boris Audio Works sound pack as the 737-700.

### Set 1 of 5

**Applies to: PMDG 737-800 BW HD, PMDG 737-800 SSW HD**

| Key | View | Seat | Where it sits | Facing |
| --- | --- | --- | --- | --- |
| Alt+1 | Engine front (left) | 7A | 8.2 m behind the pilot, 1.77 m out from the centreline | 121° left of the nose, 28° down |
| Alt+2 | Over the wing (left) | 15A | 13.6 m behind the pilot, 1.55 m out from the centreline | 92° left of the nose, 14° down |
| Alt+3 | Wing (left) | 18A | 16.9 m behind the pilot, 1.55 m out from the centreline | 62° left of the nose, 13° down |
| Alt+4 | Behind the wing (left) | 23A | 20.0 m behind the pilot, 1.55 m out from the centreline | 65° left of the nose, 12° down |
| Alt+5 | Engine front (right) | 7F | 8.2 m behind the pilot, 1.77 m out from the centreline | 121° right of the nose, 28° down |
| Alt+6 | Over the wing (right) | 15F | 13.6 m behind the pilot, 1.55 m out from the centreline | 92° right of the nose, 14° down |
| Alt+7 | Wing (right) | 18F | 16.9 m behind the pilot, 1.55 m out from the centreline | 62° right of the nose, 13° down |
| Alt+8 | Behind the wing (right) | 23F | 20.0 m behind the pilot, 1.55 m out from the centreline | 65° right of the nose, 12° down |
| Alt+9 | Pilot seat | Captain's seat | The pilot's seat | straight ahead, 11° down |
| Alt+0 | Windshield GoPro | Cockpit, at the windshield | 0.57 m ahead of the pilot's eye, 0.25 m left of centre | straight ahead, 8° down |

### Set 2 of 5

**Applies to: PMDG 737-800 BW SC, PMDG 737-800 SSW SC**

| Key | View | Seat | Where it sits | Facing |
| --- | --- | --- | --- | --- |
| Alt+1 | Engine front (left) | 7A | 8.2 m behind the pilot, 1.77 m out from the centreline | 121° left of the nose, 28° down |
| Alt+2 | Over the wing (left) | 14A | 13.6 m behind the pilot, 1.55 m out from the centreline | 92° left of the nose, 14° down |
| Alt+3 | Wing (left) | 17A | 16.9 m behind the pilot, 1.55 m out from the centreline | 62° left of the nose, 13° down |
| Alt+4 | Behind the wing (left) | 21A | 20.0 m behind the pilot, 1.55 m out from the centreline | 65° left of the nose, 12° down |
| Alt+5 | Engine front (right) | 7F | 8.2 m behind the pilot, 1.77 m out from the centreline | 121° right of the nose, 28° down |
| Alt+6 | Over the wing (right) | 14F | 13.6 m behind the pilot, 1.55 m out from the centreline | 92° right of the nose, 14° down |
| Alt+7 | Wing (right) | 17F | 16.9 m behind the pilot, 1.55 m out from the centreline | 62° right of the nose, 13° down |
| Alt+8 | Behind the wing (right) | 21F | 20.0 m behind the pilot, 1.55 m out from the centreline | 65° right of the nose, 12° down |
| Alt+9 | Pilot seat | Captain's seat | The pilot's seat | straight ahead, 11° down |
| Alt+0 | Windshield GoPro | Cockpit, at the windshield | 0.57 m ahead of the pilot's eye, 0.25 m left of centre | straight ahead, 8° down |

### Set 3 of 5

**Applies to: PMDG 737-800 BW TC, PMDG 737-800 SSW TC**

| Key | View | Seat | Where it sits | Facing |
| --- | --- | --- | --- | --- |
| Alt+1 | Engine front (left) | 6A | 8.2 m behind the pilot, 1.77 m out from the centreline | 121° left of the nose, 28° down |
| Alt+2 | Over the wing (left) | 13A | 13.6 m behind the pilot, 1.55 m out from the centreline | 92° left of the nose, 14° down |
| Alt+3 | Wing (left) | 17A | 16.9 m behind the pilot, 1.55 m out from the centreline | 62° left of the nose, 13° down |
| Alt+4 | Behind the wing (left) | 21A | 20.0 m behind the pilot, 1.55 m out from the centreline | 65° left of the nose, 12° down |
| Alt+5 | Engine front (right) | 6F | 8.2 m behind the pilot, 1.77 m out from the centreline | 121° right of the nose, 28° down |
| Alt+6 | Over the wing (right) | 13F | 13.6 m behind the pilot, 1.55 m out from the centreline | 92° right of the nose, 14° down |
| Alt+7 | Wing (right) | 17F | 16.9 m behind the pilot, 1.55 m out from the centreline | 62° right of the nose, 13° down |
| Alt+8 | Behind the wing (right) | 21F | 20.0 m behind the pilot, 1.55 m out from the centreline | 65° right of the nose, 12° down |
| Alt+9 | Pilot seat | Captain's seat | The pilot's seat | straight ahead, 11° down |
| Alt+0 | Windshield GoPro | Cockpit, at the windshield | 0.57 m ahead of the pilot's eye, 0.25 m left of centre | straight ahead, 8° down |

### Set 4 of 5

**Applies to: PMDG 737-800BCF BW, PMDG 737-800BCF SSW, PMDG 737-800BDSF BW, PMDG 737-800BDSF SSW**

| Key | View | Seat | Where it sits | Facing |
| --- | --- | --- | --- | --- |
| Alt+1 | Engine front (left) | no seats (cargo deck) | 7.8 m behind the pilot, 1.40 m out from the centreline | 120° left of the nose, 20° down |
| Alt+2 | Over the wing (left) | no seats (cargo deck) | 14.8 m behind the pilot, 1.55 m out from the centreline | 92° left of the nose, 14° down |
| Alt+3 | Wing (left) | no seats (cargo deck) | 17.0 m behind the pilot, 1.40 m out from the centreline | 62° left of the nose, 13° down |
| Alt+4 | Behind the wing (left) | no seats (cargo deck) | 20.0 m behind the pilot, 1.40 m out from the centreline | 65° left of the nose, 12° down |
| Alt+5 | Engine front (right) | no seats (cargo deck) | 7.8 m behind the pilot, 1.55 m out from the centreline | 120° right of the nose, 20° down |
| Alt+6 | Over the wing (right) | no seats (cargo deck) | 14.8 m behind the pilot, 1.55 m out from the centreline | 92° right of the nose, 14° down |
| Alt+7 | Wing (right) | no seats (cargo deck) | 17.0 m behind the pilot, 1.55 m out from the centreline | 62° right of the nose, 13° down |
| Alt+8 | Behind the wing (right) | no seats (cargo deck) | 20.0 m behind the pilot, 1.55 m out from the centreline | 65° right of the nose, 12° down |
| Alt+9 | Pilot seat | Captain's seat | The pilot's seat | straight ahead, 11° down |
| Alt+0 | Windshield GoPro | Cockpit, at the windshield | 0.57 m ahead of the pilot's eye, 0.25 m left of centre | straight ahead, 8° down |

### Set 5 of 5

**Applies to: PMDG 737-BBJ2 BW, PMDG 737-BBJ2 SSW**

| Key | View | Seat | Where it sits | Facing |
| --- | --- | --- | --- | --- |
| Alt+1 | Engine front (left) | VIP cabin (no numbered rows) | 8.2 m behind the pilot, 1.77 m out from the centreline | 121° left of the nose, 29° down |
| Alt+2 | Over the wing (left) | VIP cabin (no numbered rows) | 13.6 m behind the pilot, 1.55 m out from the centreline | 92° left of the nose, 14° down |
| Alt+3 | Wing (left) | VIP cabin (no numbered rows) | 16.9 m behind the pilot, 1.55 m out from the centreline | 62° left of the nose, 13° down |
| Alt+4 | Behind the wing (left) | VIP cabin (no numbered rows) | 20.0 m behind the pilot, 1.55 m out from the centreline | 65° left of the nose, 12° down |
| Alt+5 | Engine front (right) | VIP cabin (no numbered rows) | 8.2 m behind the pilot, 1.78 m out from the centreline | 121° right of the nose, 29° down |
| Alt+6 | Over the wing (right) | VIP cabin (no numbered rows) | 13.6 m behind the pilot, 1.55 m out from the centreline | 92° right of the nose, 14° down |
| Alt+7 | Wing (right) | VIP cabin (no numbered rows) | 17.9 m behind the pilot, 1.70 m out from the centreline | 72° right of the nose, 13° down |
| Alt+8 | Behind the wing (right) | VIP cabin (no numbered rows) | 20.0 m behind the pilot, 1.55 m out from the centreline | 65° right of the nose, 12° down |
| Alt+9 | Pilot seat | Captain's seat | The pilot's seat | straight ahead, 11° down |
| Alt+0 | Windshield GoPro | Cockpit, at the windshield | 0.57 m ahead of the pilot's eye, 0.25 m left of centre | straight ahead, 8° down |

## PMDG 737-900

**Status:** Checked in the sim on the 900ER. The engine-front views sit right up against the window, a few rows ahead of the engine.

**Sound:** Same Boris Audio Works sound pack as the 737-700.

### Set 1 of 4

**Applies to: PMDG 737-900 BW SC, PMDG 737-900 BW TC, PMDG 737-900 SSW SC, PMDG 737-900 SSW TC**

| Key | View | Seat | Where it sits | Facing |
| --- | --- | --- | --- | --- |
| Alt+1 | Engine front (left) | 8A | 9.8 m behind the pilot, 1.77 m out from the centreline | 121° left of the nose, 28° down |
| Alt+2 | Over the wing (left) | 15A | 15.2 m behind the pilot, 1.55 m out from the centreline | 92° left of the nose, 14° down |
| Alt+3 | Wing (left) | 19A | 18.4 m behind the pilot, 1.55 m out from the centreline | 62° left of the nose, 13° down |
| Alt+4 | Behind the wing (left) | 23A | 21.6 m behind the pilot, 1.55 m out from the centreline | 65° left of the nose, 12° down |
| Alt+5 | Engine front (right) | 8F | 9.8 m behind the pilot, 1.77 m out from the centreline | 121° right of the nose, 28° down |
| Alt+6 | Over the wing (right) | 15F | 15.2 m behind the pilot, 1.55 m out from the centreline | 92° right of the nose, 14° down |
| Alt+7 | Wing (right) | 19F | 18.4 m behind the pilot, 1.55 m out from the centreline | 62° right of the nose, 13° down |
| Alt+8 | Behind the wing (right) | 23F | 21.6 m behind the pilot, 1.55 m out from the centreline | 65° right of the nose, 12° down |
| Alt+9 | Pilot seat | Captain's seat | The pilot's seat | straight ahead, 11° down |
| Alt+0 | Windshield GoPro | Cockpit, at the windshield | 0.60 m ahead of the pilot's eye, 0.25 m left of centre | straight ahead, 8° down |

### Set 2 of 4

**Applies to: PMDG 737-900ER BW HD, PMDG 737-900ER SSW HD**

| Key | View | Seat | Where it sits | Facing |
| --- | --- | --- | --- | --- |
| Alt+1 | Engine front (left) | 9A | 9.8 m behind the pilot, 1.77 m out from the centreline | 121° left of the nose, 28° down |
| Alt+2 | Over the wing (left) | 17A | 15.2 m behind the pilot, 1.55 m out from the centreline | 92° left of the nose, 14° down |
| Alt+3 | Wing (left) | 21A | 18.4 m behind the pilot, 1.55 m out from the centreline | 62° left of the nose, 13° down |
| Alt+4 | Behind the wing (left) | 25A | 21.6 m behind the pilot, 1.55 m out from the centreline | 65° left of the nose, 12° down |
| Alt+5 | Engine front (right) | 9F | 9.8 m behind the pilot, 1.77 m out from the centreline | 121° right of the nose, 28° down |
| Alt+6 | Over the wing (right) | 17F | 15.2 m behind the pilot, 1.55 m out from the centreline | 92° right of the nose, 14° down |
| Alt+7 | Wing (right) | 21F | 18.4 m behind the pilot, 1.55 m out from the centreline | 62° right of the nose, 13° down |
| Alt+8 | Behind the wing (right) | 25F | 21.6 m behind the pilot, 1.55 m out from the centreline | 65° right of the nose, 12° down |
| Alt+9 | Pilot seat | Captain's seat | The pilot's seat | straight ahead, 11° down |
| Alt+0 | Windshield GoPro | Cockpit, at the windshield | 0.60 m ahead of the pilot's eye, 0.25 m left of centre | straight ahead, 8° down |

### Set 3 of 4

**Applies to: PMDG 737-900ER BW SC, PMDG 737-900ER SSW SC**

| Key | View | Seat | Where it sits | Facing |
| --- | --- | --- | --- | --- |
| Alt+1 | Engine front (left) | 9A | 9.8 m behind the pilot, 1.77 m out from the centreline | 121° left of the nose, 28° down |
| Alt+2 | Over the wing (left) | 16A | 15.2 m behind the pilot, 1.55 m out from the centreline | 92° left of the nose, 14° down |
| Alt+3 | Wing (left) | 19A | 18.4 m behind the pilot, 1.55 m out from the centreline | 62° left of the nose, 13° down |
| Alt+4 | Behind the wing (left) | 23A | 21.6 m behind the pilot, 1.55 m out from the centreline | 65° left of the nose, 12° down |
| Alt+5 | Engine front (right) | 9F | 9.8 m behind the pilot, 1.77 m out from the centreline | 121° right of the nose, 28° down |
| Alt+6 | Over the wing (right) | 16F | 15.2 m behind the pilot, 1.55 m out from the centreline | 92° right of the nose, 14° down |
| Alt+7 | Wing (right) | 19F | 18.4 m behind the pilot, 1.55 m out from the centreline | 62° right of the nose, 13° down |
| Alt+8 | Behind the wing (right) | 23F | 21.6 m behind the pilot, 1.55 m out from the centreline | 65° right of the nose, 12° down |
| Alt+9 | Pilot seat | Captain's seat | The pilot's seat | straight ahead, 11° down |
| Alt+0 | Windshield GoPro | Cockpit, at the windshield | 0.60 m ahead of the pilot's eye, 0.25 m left of centre | straight ahead, 8° down |

### Set 4 of 4

**Applies to: PMDG 737-900ER BW TC, PMDG 737-900ER SSW TC**

| Key | View | Seat | Where it sits | Facing |
| --- | --- | --- | --- | --- |
| Alt+1 | Engine front (left) | 8A | 9.8 m behind the pilot, 1.77 m out from the centreline | 121° left of the nose, 28° down |
| Alt+2 | Over the wing (left) | 15A | 15.2 m behind the pilot, 1.55 m out from the centreline | 92° left of the nose, 14° down |
| Alt+3 | Wing (left) | 18A | 18.4 m behind the pilot, 1.55 m out from the centreline | 62° left of the nose, 13° down |
| Alt+4 | Behind the wing (left) | 22A | 21.6 m behind the pilot, 1.55 m out from the centreline | 65° left of the nose, 12° down |
| Alt+5 | Engine front (right) | 8F | 9.8 m behind the pilot, 1.77 m out from the centreline | 121° right of the nose, 28° down |
| Alt+6 | Over the wing (right) | 15F | 15.2 m behind the pilot, 1.55 m out from the centreline | 92° right of the nose, 14° down |
| Alt+7 | Wing (right) | 18F | 18.4 m behind the pilot, 1.55 m out from the centreline | 62° right of the nose, 13° down |
| Alt+8 | Behind the wing (right) | 22F | 21.6 m behind the pilot, 1.55 m out from the centreline | 65° right of the nose, 12° down |
| Alt+9 | Pilot seat | Captain's seat | The pilot's seat | straight ahead, 11° down |
| Alt+0 | Windshield GoPro | Cockpit, at the windshield | 0.60 m ahead of the pilot's eye, 0.25 m left of centre | straight ahead, 8° down |

## Fenix A319

**Status:** Uses the same seats as the A320, measured from the wing. Not loaded in the sim.

**Sound:** Taken from the Fenix's own sound files. Each engine plays from one point in the middle of the engine. Alt+2/6 are the closest seats to that point and to the barking-dog pump (PTU), the air conditioning packs, the fuel pumps and the slats. Alt+3/7 sit over the flaps and main gear, right above the touchdown thumps and flap rumble. Alt+4/8 is the quietest cabin seat, next to the cabin air sound, because the Fenix has no separate exhaust sound. Outside-only sounds, such as exterior wind, brakes and gear doors, can't be heard from the cabin views. Alt+9 and Alt+0 are cockpit views and hear the cockpit as normal.

**Applies to: FNX_319_CFM_SL_HD, FNX_319_CFM_SL_SD, FNX_319_CFM_WF_HD, FNX_319_CFM_WF_SD, FNX_319_IAE_SL_HD, FNX_319_IAE_SL_SD, FNX_319_IAE_WF_HD, FNX_319_IAE_WF_SD**

| Key | View | Seat | Where it sits | Facing |
| --- | --- | --- | --- | --- |
| Alt+1 | Engine front (left) | 2A | 4.1 m behind the pilot, 1.82 m out from the centreline | 122° left of the nose, 27° down |
| Alt+2 | Over the wing (left) | 10A | 10.3 m behind the pilot, 1.80 m out from the centreline | 100° left of the nose, 14° down |
| Alt+3 | Wing (left) | 15A | 13.9 m behind the pilot, 1.80 m out from the centreline | 75° left of the nose, 13° down |
| Alt+4 | Behind the wing (left) | 20A | 17.1 m behind the pilot, 1.80 m out from the centreline | 68° left of the nose, 12° down |
| Alt+5 | Engine front (right) | 2F | 4.1 m behind the pilot, 1.82 m out from the centreline | 122° right of the nose, 27° down |
| Alt+6 | Over the wing (right) | 10F | 10.3 m behind the pilot, 1.80 m out from the centreline | 100° right of the nose, 14° down |
| Alt+7 | Wing (right) | 15F | 13.9 m behind the pilot, 1.80 m out from the centreline | 75° right of the nose, 13° down |
| Alt+8 | Behind the wing (right) | 20F | 17.1 m behind the pilot, 1.80 m out from the centreline | 68° right of the nose, 12° down |
| Alt+9 | Pilot seat | Captain's seat | The pilot's seat | straight ahead, 10° down |
| Alt+0 | Windshield GoPro | Cockpit, at the windshield | 0.67 m ahead of the pilot's eye, 0.25 m left of centre | straight ahead, 8° down |

## Fenix A320

**Status:** Checked in the sim. The engine-front views sit 3 m ahead of the engines, looking back into the intakes. The A320 versions also keep an extra camera called "Pilot", which is not on an Alt key.

**Sound:** Taken from the Fenix's own sound files. Each engine plays from one point in the middle of the engine. Alt+2/6 are the closest seats to that point and to the barking-dog pump (PTU), the air conditioning packs, the fuel pumps and the slats. Alt+3/7 sit over the flaps and main gear, right above the touchdown thumps and flap rumble. Alt+4/8 is the quietest cabin seat, next to the cabin air sound, because the Fenix has no separate exhaust sound. Outside-only sounds, such as exterior wind, brakes and gear doors, can't be heard from the cabin views. Alt+9 and Alt+0 are cockpit views and hear the cockpit as normal.

**Applies to: FNX_320_CFM_SL, FNX_320_CFM_WF, FNX_320_IAE_SL, FNX_320_IAE_WF**

| Key | View | Seat | Where it sits | Facing |
| --- | --- | --- | --- | --- |
| Alt+1 | Engine front (left) | 4A | 5.7 m behind the pilot, 1.82 m out from the centreline | 122° left of the nose, 22° down |
| Alt+2 | Over the wing (left) | 12A | 11.9 m behind the pilot, 1.80 m out from the centreline | 100° left of the nose, 14° down |
| Alt+3 | Wing (left) | 17A | 15.5 m behind the pilot, 1.80 m out from the centreline | 75° left of the nose, 13° down |
| Alt+4 | Behind the wing (left) | 22A | 18.7 m behind the pilot, 1.80 m out from the centreline | 68° left of the nose, 12° down |
| Alt+5 | Engine front (right) | 4F | 5.7 m behind the pilot, 1.82 m out from the centreline | 122° right of the nose, 22° down |
| Alt+6 | Over the wing (right) | 12F | 11.9 m behind the pilot, 1.80 m out from the centreline | 100° right of the nose, 14° down |
| Alt+7 | Wing (right) | 17F | 15.5 m behind the pilot, 1.80 m out from the centreline | 75° right of the nose, 13° down |
| Alt+8 | Behind the wing (right) | 22F | 18.7 m behind the pilot, 1.80 m out from the centreline | 68° right of the nose, 12° down |
| Alt+9 | Pilot seat | Captain's seat | The pilot's seat | straight ahead, 9° down |
| Alt+0 | Windshield GoPro | Cockpit, at the windshield | 0.70 m ahead of the pilot's eye, 0.25 m left of centre | straight ahead, 8° down |

## Fenix A321

**Status:** Checked in the sim. The engine-front views sit at the window just in front of door 2. Door 3 leaves a gap in the windows, so the behind-the-wing view sits right behind the wing root.

**Sound:** Taken from the Fenix's own sound files. Each engine plays from one point in the middle of the engine. Alt+2/6 are the closest seats to that point and to the barking-dog pump (PTU), the air conditioning packs, the fuel pumps and the slats. Alt+3/7 sit over the flaps and main gear, right above the touchdown thumps and flap rumble. Alt+4/8 is the quietest cabin seat, next to the cabin air sound, because the Fenix has no separate exhaust sound. Outside-only sounds, such as exterior wind, brakes and gear doors, can't be heard from the cabin views. Alt+9 and Alt+0 are cockpit views and hear the cockpit as normal.

### Set 1 of 2

**Applies to: FNX_321_CFM_SL_SC, FNX_321_CFM_WF_SC, FNX_321_IAE_SL_SC, FNX_321_IAE_WF_SC**

| Key | View | Seat | Where it sits | Facing |
| --- | --- | --- | --- | --- |
| Alt+1 | Engine front (left) | 10A (extra legroom / exit area) | 10.0 m behind the pilot, 1.82 m out from the centreline | 122° left of the nose, 27° down |
| Alt+2 | Over the wing (left) | 16A | 16.2 m behind the pilot, 1.80 m out from the centreline | 100° left of the nose, 14° down |
| Alt+3 | Wing (left) | 21A | 19.8 m behind the pilot, 1.80 m out from the centreline | 75° left of the nose, 13° down |
| Alt+4 | Behind the wing (left) | 23A (extra legroom / exit area) | 21.4 m behind the pilot, 1.80 m out from the centreline | 68° left of the nose, 12° down |
| Alt+5 | Engine front (right) | 10F (extra legroom / exit area) | 10.0 m behind the pilot, 1.82 m out from the centreline | 122° right of the nose, 27° down |
| Alt+6 | Over the wing (right) | 16F | 16.2 m behind the pilot, 1.80 m out from the centreline | 100° right of the nose, 14° down |
| Alt+7 | Wing (right) | 21F | 19.8 m behind the pilot, 1.80 m out from the centreline | 75° right of the nose, 13° down |
| Alt+8 | Behind the wing (right) | 23F (extra legroom / exit area) | 21.4 m behind the pilot, 1.80 m out from the centreline | 68° right of the nose, 12° down |
| Alt+9 | Pilot seat | Captain's seat | The pilot's seat | straight ahead, 9° down |
| Alt+0 | Windshield GoPro | Cockpit, at the windshield | 0.66 m ahead of the pilot's eye, 0.25 m left of centre | straight ahead, 8° down |

### Set 2 of 2

**Applies to: FNX_321_CFM_SL_TC, FNX_321_CFM_WF_TC, FNX_321_IAE_SL_TC, FNX_321_IAE_WF_TC**

| Key | View | Seat | Where it sits | Facing |
| --- | --- | --- | --- | --- |
| Alt+1 | Engine front (left) | 7A (extra legroom / exit area) | 10.0 m behind the pilot, 1.82 m out from the centreline | 122° left of the nose, 27° down |
| Alt+2 | Over the wing (left) | 13A | 16.2 m behind the pilot, 1.80 m out from the centreline | 100° left of the nose, 14° down |
| Alt+3 | Wing (left) | 18A | 19.8 m behind the pilot, 1.80 m out from the centreline | 75° left of the nose, 13° down |
| Alt+4 | Behind the wing (left) | 20A | 21.4 m behind the pilot, 1.80 m out from the centreline | 68° left of the nose, 12° down |
| Alt+5 | Engine front (right) | 7F (extra legroom / exit area) | 10.0 m behind the pilot, 1.82 m out from the centreline | 122° right of the nose, 27° down |
| Alt+6 | Over the wing (right) | 13F | 16.2 m behind the pilot, 1.80 m out from the centreline | 100° right of the nose, 14° down |
| Alt+7 | Wing (right) | 18F | 19.8 m behind the pilot, 1.80 m out from the centreline | 75° right of the nose, 13° down |
| Alt+8 | Behind the wing (right) | 20F | 21.4 m behind the pilot, 1.80 m out from the centreline | 68° right of the nose, 12° down |
| Alt+9 | Pilot seat | Captain's seat | The pilot's seat | straight ahead, 9° down |
| Alt+0 | Windshield GoPro | Cockpit, at the windshield | 0.66 m ahead of the pilot's eye, 0.25 m left of centre | straight ahead, 8° down |

## FlyByWire A32NX

**Status:** Checked in the sim. This aircraft has no cabin model and its windows are painted on, so the cabin views look out through the side of the fuselage.

**Sound:** Each engine has separate front and rear sounds, played from its fan. The barking-dog pump and the electric hydraulic pumps play just behind Alt+2/6, the slats near Alt+6 on the right, and the flap motor beside Alt+4 on the left.

**File: FlyByWire_A320_NEO**

| Key | View | Seat | Where it sits | Facing |
| --- | --- | --- | --- | --- |
| Alt+1 | Engine front (left) | 3A (Fenix A320 rows; no seats modelled) | 5.4 m behind the pilot, 1.87 m out from the centreline | 132° left of the nose, 23° down |
| Alt+2 | Over the wing (left) | 12A (Fenix A320 rows; no seats modelled) | 12.1 m behind the pilot, 1.81 m out from the centreline | 100° left of the nose, 14° down |
| Alt+3 | Wing (left) | 17A (Fenix A320 rows; no seats modelled) | 15.7 m behind the pilot, 1.81 m out from the centreline | 75° left of the nose, 13° down |
| Alt+4 | Behind the wing (left) | 22A (Fenix A320 rows; no seats modelled) | 18.9 m behind the pilot, 1.89 m out from the centreline | 60° left of the nose, 12° down |
| Alt+5 | Engine front (right) | 3F (Fenix A320 rows; no seats modelled) | 5.4 m behind the pilot, 1.89 m out from the centreline | 138° right of the nose, 23° down |
| Alt+6 | Over the wing (right) | 12F (Fenix A320 rows; no seats modelled) | 12.1 m behind the pilot, 1.81 m out from the centreline | 100° right of the nose, 14° down |
| Alt+7 | Wing (right) | 17F (Fenix A320 rows; no seats modelled) | 15.7 m behind the pilot, 1.81 m out from the centreline | 75° right of the nose, 13° down |
| Alt+8 | Behind the wing (right) | 22F (Fenix A320 rows; no seats modelled) | 18.9 m behind the pilot, 1.89 m out from the centreline | 60° right of the nose, 12° down |
| Alt+9 | Pilot seat | Captain's seat | The pilot's seat | straight ahead, 12° down |
| Alt+0 | Windshield GoPro | Cockpit, at the windshield | 0.64 m ahead of the pilot's eye, 0.25 m left of centre | straight ahead, 8° down |

## iFly 737 MAX 8

**Status:** Checked in the sim. All ten views were checked on the 189-seat and the MAX 8200, and the new engine-front views on the MAX 8200 and the 166-seat. The 178-seat uses the same seats as the 189-seat.

**Sound:** Each engine has separate front and rear sounds, played from its fan. The hydraulic and flap sounds play from the middle of the aircraft, over the wing, nearest Alt+2/6.

### Set 1 of 4

**Applies to: iFly 737-MAX8-166Seats**

| Key | View | Seat | Where it sits | Facing |
| --- | --- | --- | --- | --- |
| Alt+1 | Engine front (left) | 5A | 7.6 m behind the pilot, 1.74 m out from the centreline | 127° left of the nose, 23° down |
| Alt+2 | Over the wing (left) | 15A | 15.7 m behind the pilot, 1.60 m out from the centreline | 100° left of the nose, 14° down |
| Alt+3 | Wing (left) | 19A | 18.4 m behind the pilot, 1.60 m out from the centreline | 83° left of the nose, 13° down |
| Alt+4 | Behind the wing (left) | 21A | 20.5 m behind the pilot, 1.60 m out from the centreline | 76° left of the nose, 12° down |
| Alt+5 | Engine front (right) | 5F | 7.6 m behind the pilot, 1.74 m out from the centreline | 127° right of the nose, 23° down |
| Alt+6 | Over the wing (right) | 15F | 15.7 m behind the pilot, 1.60 m out from the centreline | 100° right of the nose, 14° down |
| Alt+7 | Wing (right) | 19F | 18.4 m behind the pilot, 1.60 m out from the centreline | 83° right of the nose, 13° down |
| Alt+8 | Behind the wing (right) | 21F | 20.5 m behind the pilot, 1.60 m out from the centreline | 76° right of the nose, 12° down |
| Alt+9 | Pilot seat | Captain's seat | The pilot's seat | straight ahead, 14° down |
| Alt+0 | Windshield GoPro | Cockpit, at the windshield | 0.66 m ahead of the pilot's eye, 0.25 m left of centre | straight ahead, 8° down |

### Set 2 of 4

**Applies to: iFly 737-MAX8-189Seats**

| Key | View | Seat | Where it sits | Facing |
| --- | --- | --- | --- | --- |
| Alt+1 | Engine front (left) | 7A | 7.6 m behind the pilot, 1.74 m out from the centreline | 127° left of the nose, 23° down |
| Alt+2 | Over the wing (left) | 17A | 15.7 m behind the pilot, 1.60 m out from the centreline | 100° left of the nose, 14° down |
| Alt+3 | Wing (left) | 20A | 17.9 m behind the pilot, 1.60 m out from the centreline | 83° left of the nose, 13° down |
| Alt+4 | Behind the wing (left) | 24A | 21.1 m behind the pilot, 1.60 m out from the centreline | 76° left of the nose, 12° down |
| Alt+5 | Engine front (right) | 7F | 7.6 m behind the pilot, 1.74 m out from the centreline | 127° right of the nose, 23° down |
| Alt+6 | Over the wing (right) | 17F | 15.7 m behind the pilot, 1.60 m out from the centreline | 100° right of the nose, 14° down |
| Alt+7 | Wing (right) | 20F | 17.9 m behind the pilot, 1.60 m out from the centreline | 83° right of the nose, 13° down |
| Alt+8 | Behind the wing (right) | 24F | 21.1 m behind the pilot, 1.60 m out from the centreline | 76° right of the nose, 12° down |
| Alt+9 | Pilot seat | Captain's seat | The pilot's seat | straight ahead, 14° down |
| Alt+0 | Windshield GoPro | Cockpit, at the windshield | 0.66 m ahead of the pilot's eye, 0.25 m left of centre | straight ahead, 8° down |

### Set 3 of 4

**Applies to: iFly 737-MAX8200**

| Key | View | Seat | Where it sits | Facing |
| --- | --- | --- | --- | --- |
| Alt+1 | Engine front (left) | 6A | 7.6 m behind the pilot, 1.74 m out from the centreline | 127° left of the nose, 23° down |
| Alt+2 | Over the wing (left) | 14A | 13.6 m behind the pilot, 1.60 m out from the centreline | 84° left of the nose, 14° down |
| Alt+3 | Wing (left) | 20A | 18.4 m behind the pilot, 1.60 m out from the centreline | 83° left of the nose, 13° down |
| Alt+4 | Behind the wing (left) | 24A | 21.1 m behind the pilot, 1.60 m out from the centreline | 76° left of the nose, 12° down |
| Alt+5 | Engine front (right) | 6F | 7.6 m behind the pilot, 1.74 m out from the centreline | 127° right of the nose, 23° down |
| Alt+6 | Over the wing (right) | 14F | 13.6 m behind the pilot, 1.60 m out from the centreline | 84° right of the nose, 14° down |
| Alt+7 | Wing (right) | 20F | 18.4 m behind the pilot, 1.60 m out from the centreline | 83° right of the nose, 13° down |
| Alt+8 | Behind the wing (right) | 24F | 21.1 m behind the pilot, 1.60 m out from the centreline | 76° right of the nose, 12° down |
| Alt+9 | Pilot seat | Captain's seat | The pilot's seat | straight ahead, 14° down |
| Alt+0 | Windshield GoPro | Cockpit, at the windshield | 0.66 m ahead of the pilot's eye, 0.25 m left of centre | straight ahead, 8° down |

### Set 4 of 4

**Applies to: iFly 737-MAX8**

| Key | View | Seat | Where it sits | Facing |
| --- | --- | --- | --- | --- |
| Alt+1 | Engine front (left) | 5A | 7.6 m behind the pilot, 1.74 m out from the centreline | 127° left of the nose, 23° down |
| Alt+2 | Over the wing (left) | 16A | 15.7 m behind the pilot, 1.60 m out from the centreline | 100° left of the nose, 14° down |
| Alt+3 | Wing (left) | 19A | 17.9 m behind the pilot, 1.60 m out from the centreline | 83° left of the nose, 13° down |
| Alt+4 | Behind the wing (left) | 22A | 20.0 m behind the pilot, 1.60 m out from the centreline | 76° left of the nose, 12° down |
| Alt+5 | Engine front (right) | 5F | 7.6 m behind the pilot, 1.74 m out from the centreline | 127° right of the nose, 23° down |
| Alt+6 | Over the wing (right) | 16F | 15.7 m behind the pilot, 1.60 m out from the centreline | 100° right of the nose, 14° down |
| Alt+7 | Wing (right) | 19F | 17.9 m behind the pilot, 1.60 m out from the centreline | 83° right of the nose, 13° down |
| Alt+8 | Behind the wing (right) | 22F | 20.0 m behind the pilot, 1.60 m out from the centreline | 76° right of the nose, 12° down |
| Alt+9 | Pilot seat | Captain's seat | The pilot's seat | straight ahead, 14° down |
| Alt+0 | Windshield GoPro | Cockpit, at the windshield | 0.66 m ahead of the pilot's eye, 0.25 m left of centre | straight ahead, 8° down |

## TFDi MD-11F

**Status:** Views by wolfman1360, checked against TFDi's own 3D model but not yet loaded in the sim. Identical on the GE and PW versions, with and without the LOW option. The freighter has only two windows on each side, and the views over the wing and on the wing (Alt+2/3/6/7) look out of them. The engine-front and behind-the-wing views have no window and face the cargo-deck wall, so they're for sound only. The engine-front views sit 4.5 m ahead of the intake. The pilot seat is TFDi's own pilot view, which looks 2° up.

**Sound:** TFDi's own sound set by Echo19 Audio, plus the aek sound MD-11 pack if it's installed. Each wing engine plays from one point at the back of the engine, so Alt+2/6 are the closest seats to it. The hydraulic pumps, flaps, landing gear and touchdowns play from the middle of the aircraft, about 3 m behind Alt+2/6. The air conditioning packs play at the front, near the cockpit. The third engine and the APU play from the tail, more than 20 m behind every cabin view; Alt+4/8 are the closest. Alt+9 and Alt+0 are cockpit views and hear the cockpit as normal.

**Applies to: TFDi_Design_MD-11F GE, TFDi_Design_MD-11F GE LOW, TFDi_Design_MD-11F PW, TFDi_Design_MD-11F PW LOW**

| Key | View | Seat | Where it sits | Facing |
| --- | --- | --- | --- | --- |
| Alt+1 | Engine front (left) | no seats (cargo deck) | 16.4 m behind the pilot, 2.43 m out from the centreline | 133° left of the nose, 24° down |
| Alt+2 | Over the wing (left) | no seats (cargo deck) | 22.8 m behind the pilot, 2.88 m out from the centreline | 100° left of the nose, 14° down |
| Alt+3 | Wing (left) | no seats (cargo deck) | 33.0 m behind the pilot, 2.80 m out from the centreline | 83° left of the nose, 13° down |
| Alt+4 | Behind the wing (left) | no seats (cargo deck) | 35.7 m behind the pilot, 2.43 m out from the centreline | 65° left of the nose, 12° down |
| Alt+5 | Engine front (right) | no seats (cargo deck) | 16.4 m behind the pilot, 2.43 m out from the centreline | 133° right of the nose, 24° down |
| Alt+6 | Over the wing (right) | no seats (cargo deck) | 22.8 m behind the pilot, 2.88 m out from the centreline | 100° right of the nose, 14° down |
| Alt+7 | Wing (right) | no seats (cargo deck) | 33.0 m behind the pilot, 2.88 m out from the centreline | 83° right of the nose, 13° down |
| Alt+8 | Behind the wing (right) | no seats (cargo deck) | 35.7 m behind the pilot, 2.43 m out from the centreline | 65° right of the nose, 12° down |
| Alt+9 | Pilot seat | Captain's seat | The pilot's seat | straight ahead, 2° up |
| Alt+0 | Windshield GoPro | Cockpit, at the windshield | 0.77 m ahead of the pilot's eye, 0.25 m left of centre | straight ahead, 8° down |

## TFDi MD-11

**Status:** Views by wolfman1360, the same as the MD-11F, as it's the same airframe. Not checked: the passenger cabin isn't installed on the PC these notes were written on. TFDi doesn't publish its seat map, so the Seat column gives each view's distance from the nearest passenger door instead, using the door positions in Boeing's MD-11 airport-planning document (door 1 in TFDi's model matches it to 3 cm). The views over the wing and on the wing (Alt+2/3/6/7) sit close to the glass at the freighter's window positions. The engine-front and behind-the-wing views sit about 0.6 m in from the wall, where a seat may be in the way. Try them all in the sim before relying on them.

**Sound:** Same sound set as the MD-11F.

**Applies to: TFDi_Design_MD-11 GE, TFDi_Design_MD-11 GE LOW, TFDi_Design_MD-11 PW, TFDi_Design_MD-11 PW LOW**

| Key | View | Seat | Where it sits | Facing |
| --- | --- | --- | --- | --- |
| Alt+1 | Engine front (left) | about 4 m behind door 2 | 16.4 m behind the pilot, 2.43 m out from the centreline | 133° left of the nose, 24° down |
| Alt+2 | Over the wing (left) | about 4 m ahead of door 3 (the overwing door) | 22.8 m behind the pilot, 2.88 m out from the centreline | 100° left of the nose, 14° down |
| Alt+3 | Wing (left) | about 6 m behind door 3 | 33.0 m behind the pilot, 2.80 m out from the centreline | 83° left of the nose, 13° down |
| Alt+4 | Behind the wing (left) | about 9 m behind door 3, midway to door 4 | 35.7 m behind the pilot, 2.43 m out from the centreline | 65° left of the nose, 12° down |
| Alt+5 | Engine front (right) | about 4 m behind door 2 | 16.4 m behind the pilot, 2.43 m out from the centreline | 133° right of the nose, 24° down |
| Alt+6 | Over the wing (right) | about 4 m ahead of door 3 (the overwing door) | 22.8 m behind the pilot, 2.88 m out from the centreline | 100° right of the nose, 14° down |
| Alt+7 | Wing (right) | about 6 m behind door 3 | 33.0 m behind the pilot, 2.88 m out from the centreline | 83° right of the nose, 13° down |
| Alt+8 | Behind the wing (right) | about 9 m behind door 3, midway to door 4 | 35.7 m behind the pilot, 2.43 m out from the centreline | 65° right of the nose, 12° down |
| Alt+9 | Pilot seat | Captain's seat | The pilot's seat | straight ahead, 2° up |
| Alt+0 | Windshield GoPro | Cockpit, at the windshield | 0.77 m ahead of the pilot's eye, 0.25 m left of centre | straight ahead, 8° down |
