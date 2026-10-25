# Bến Không Tên — Game design, development edition

## Intent and delivered scope

An adult revisits a childhood neighbourhood and discovers that “everyone left voluntarily” was a convenient story supported by altered school records and a diverted payment. The central interaction is checking claims against evidence, then choosing how to tell a story without taking agency from its subjects.

Delivered: a compact, complete narrative arc implemented across five small 3D areas, twenty sequential deductions and three consequence scenes. Target release: a more detailed 4–6 hour experience. The target duration has not been measured or achieved. The current question-based investigations and generated environments are an early production foundation, not final art or a finished commercial game.

## Loop and spatial design

Explore with a first-person camera → read tangible records → review the journal → compare evidence at the deduction board → solve → talk to witnesses → leave through a marked door. Documents persist across chapters. Locked questions state missing evidence. Each offers two hints. Mistakes are recoverable and never destroy evidence. All clues and exit paths are reachable under the collision model; this was checked with a grid traversal in all five areas.

1. Courtyard: chairs, bicycle, tea table, veranda, laundry and calendar. A welcoming return undermined by a dated photograph. Code, memory contradiction and document selection.
2. School: desks, blackboard and shuttered windows. A teacher’s small falsification reveals forced relocation. Attendance comparison, carbon-paper order and linked records.
3. Wharf: dock boards, water surface, boat and rain ambience. A blamed ferryman becomes a witness. Radio transcript frequency, time interval and corroborated arrival.
4. Archive: shelves and paper stacks. The protagonist’s mother benefited from falsification. Payment arithmetic, cross-chapter contradiction and responsibility inference.
5. Warehouse: stored boxes, dock and two characters. The subject of the investigation asks for control over her own account. Redaction, evidence chain and custody, followed by an ethical decision.

The areas currently share a veranda shell. Fully distinct architectural layouts, material art, inspectable objects, environmental animations and additional optional routes remain production work.

## Puzzle dependency graph

Within each chapter, all its document nodes can be collected in any order. Puzzle order is enforced:

`calendar → tin → memory (+photo) → route (+letter)`

`register + attendance → absence → copy (+carbon) → school`

`radio → tune → time (+ferry) → witness (+receipt)`

`ledger → money → claim (+petition +photo from chapter 1) → drawing (+draft)`

`lan + editor → redact → chain (+ledger +carbon) → custody (+nhi)`

All four solved → chapter exit. Full final chapter → ending choice. Together additionally requires quotation approval from Hạnh and Lan. Consent may be revisited through the journal to avoid an irreversible dialogue softlock. The current board presents explicit connections as answer choices; freeform draggable pins are not implemented.

## Presentation and technical design

Python 3.12/Panda3D. Original deterministic textured low-poly geometry; one area resident at a time. Simple horizontal capsule-like radius against rectangular obstacles; boundary containment; axis-separated sliding. Camera near clipping, pitch limits, normalized diagonal speed, run/crouch and optional low-amplitude bob. Animated fans and NPC facing/idle movement. Static ambient/directional lighting and fog. Low/Medium/High currently control viewing distance only.

Minimal exploration HUD with crosshair and nearby interaction prompt. Modal evidence, dialogue, map, puzzles, settings and save slots pause movement. Keyboard and mouse input, with arrow-key look fallback. No gamepad support or rebinding yet. Menu uses the actual 3D scene as backdrop.

Original synthesized music, rain, footsteps, paper and discovery tones. No voice acting; dialogue is readable text. One music loop is shared across the story; ending-specific score and positional ambience are not yet produced. The radio puzzle is solved using its transcript, not recorded speech recognition.

## Localization and persistence

Vietnamese default. English available in Settings; world labels are rebuilt on change. UI keys in `source/locale.py`; all story strings in `data/story.json` have `vi` and `en`. DejaVu Sans is included with its license and supports Vietnamese diacritics. Numbers, names and control key names are shared where appropriate.

Versioned JSON autosave plus three manual slots. Atomic file replacement, preservation of the previous valid save, fallback to backup, dependency validation on load. Stores chapter, position/heading, clues, solved puzzles, witness consent, decisions and ending. Settings are a separate per-user file. Saves survive relocation of the installation.

## Revision 0.2

A fourth ordering deduction follows each chapter’s three initial deductions. The evidence board now supports draggable cards, validated pair connections and saved positions; inspection renders a rotatable paper object. Chapter replay isolates the campaign save. Key use opens the archive drawer and reveals the draft. Category volume controls and five-action rebinding work. Nine short original score cues replace the single shared loop for menus, chapters and endings. These additions do not establish the target playtime or final art quality; details and remaining limits are in docs/REQUIREMENTS_STATUS.md.
