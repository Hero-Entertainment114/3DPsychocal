# Test report — 2026-10-25

## Environment and status

Linux x86_64, Python 3.12.14, Panda3D 1.10.16, Pillow 11.3.0, pytest 8.4.2. Rendering used Mesa EGL surfaceless/offscreen at 1280×720 with a null audio backend. No Windows host or target Intel UHD 620 was available. This is a development build, not a validated Windows release.

## Executed and passed

- `python -m pytest -q`: **22 passed**, no skips. Tests cover all 15 puzzle dependencies and completion, required evidence and order, recoverable wrong answers, three distinct endings, late witness consent, chapter transitions, four save slots, round-trip state, corrupt-primary fallback and invalid-state rejection.
- `python tools/render_validation.py /tmp/ben-validation`: **passed** for both languages. Instantiated the actual Panda3D application, rendered all five chapter scenes in each language, exercised forward movement and crouch through the game task, opened each evidence document, submitted wrong and correct answers to all fifteen UI puzzles per language, spoke with witnesses, saved/loaded each chapter and triggered all three endings in each language. **102 screenshots** were produced in that run, all 1280×720.
- Grid traversal checked reachability of all interaction targets in every area under the implemented collision rectangles; exterior bounds reject movement. This is useful navigation validation, not a complete manual collision audit.
- Separate settings integration check: switched Vietnamese to English through the real setting callback, changed quality, bob and FOV, wrote settings, destroyed/recreated the game and verified persistence. Font glyph lookup for all alphabetic characters in the shipped story/UI succeeded. Vietnamese screenshots were visually inspected for accents; menu and puzzle layout inspected at the default size.
- `python -m compileall -q source tools run_game.py`: passed.
- Headless smoke render loaded geometry, textures and font and produced an actual 3D frame.
- Source ZIP integrity verified, then extracted to a temporary directory and launched successfully from an unrelated working directory (`/tmp`). This verifies source resource-path independence; it does not verify a frozen Windows executable.

Corrections made during verification: copied geometry nodes instead of attaching the same node into incompatible parents; renamed an application method that shadowed Panda3D's logger; made dynamic-font initialization safe for a second application instance; preserved fractional FOV settings on reload. The affected operations were rerun successfully.

The headless renderer prints `/dev/input` device warnings because the container has no physical input device; it continues and generates the expected frames.

## Not tested / not delivered as complete

- Windows `Game.exe` build, DLL collection and clean-machine execution: **not tested**. `tools/build_windows.bat` and structural verification scripts supplied. No Windows release ZIP has been produced.
- Live keyboard/mouse capture on a desktop, physical device behaviour, fullscreen/resolution transitions and audio output: **not tested**. Integration tests call real application handlers and advance the frame loop but do not replace human playtesting.
- 30 FPS on Intel UHD 620, RAM/VRAM profiling, long sessions and 4–6 hour duration: **not tested**. No target-performance claim is made.
- Original full brief: art polish, long-form narrative, freeform evidence pinning, item rotation/use, animated drawers/doors, richer NPC animation, distinct musical scores and other production work remain. See docs/PRODUCTION_BACKLOG.md.
- External editorial/cultural review and independent translation review: **not performed**.

Selected rendered examples are in `docs/screenshots/`. All synthesized WAVs exist and contain PCM data, but their listening quality was not verified on this headless host.

## Revision 0.2 — latest verified state

Earlier 22-test / 15-puzzle figures above describe version 0.1. The following supersedes those counts:

- `python -m pytest -q`: **27 passed**, no skips. Added validation of evidence ownership/relationships, campaign-preserving replay, new save fields, v1 migration and invalid links.
- `tools/render_validation.py`: **passed**, two locales × five chapters × twenty puzzles per campaign; all three endings per language; **112 actual rendered screenshots**. A subsequent targeted cabinet regression check verified the final dynamic-node correction.
- `tools/check_features.py`: **passed** in both languages: actual document rotation, evidence linking, category volume controls, valid/invalid rebinding, rebound input dispatched through Panda3D messenger, campaign-save isolation in replay, and pause-menu time exclusion.
- `tools/check_cabinet.py`: **passed**: locked drawer prevents evidence collection, acquired key reveals the document, drawer animates to its open position, save/load restores opening, cross-page card linking works, and chapter/menu music routing changes. A failure exposed that static-geometry optimization reset the drawer transform; the animated node is now excluded and the check passes after reload.
- `tools/acceptance_assets.py`: **22 asset files** decoded/audited with SHA-256; includes six texture PNGs, fourteen PCM WAV files and font/license. This proves file integrity, not audible or artistic quality.
- Blender **4.3.2** executed `tools/design_rooms_blender.py`: five `.blend` Function proposals and twenty review renders produced. Four opening masks successfully traced using the plugin's original tracer. Actual mesh floor plan and in-game inspection screenshots were visually inspected.
- Build 3D Game Rooms Function validator: **FAILED as expected**, because human approvals and service price/budget are absent. See `production/room-review/function-validation.txt`. This is not counted as a passed gate.
- Lux3D runtime setup: **passed** using the original setup script and declared requests dependency. No API request made; keys and private configuration are absent, user reported no account. Required `body.md` resource could not be read; standalone references were available. No claim of generated Lux3D/Meshy assets.

**Still not verified:** 4–6 hour duration, Windows build/runtime, Intel UHD 620 performance, physical mouse/fullscreen/audio behaviour, final art and complete master-brief scope. No player-release EXE/ZIP is supplied. Source and editable design package only.

## Revision 0.3 checks

- Unit suite: **28 passed**. Added unique/bilingual conversation checks.
- `tools/check_dialogues.py`: all 15 conversations rendered in both languages; reading history persisted after save/load.
- Blender composition renders ran after disabling unavailable OpenImageDenoise. Five sources, 40 views. Evaluated topology/opening/contact results are in production/form-review/geometry-audit.json. These are limited geometry checks, not comprehensive Form approval.
- The user approved the five layouts and reference for local Blender only. No paid task or runtime export occurred.
- Duration, target hardware, Windows EXE and full production quality remain unverified/unfulfilled.

Final 0.3 geometry rerun: all five rooms have closed evaluated mesh topology, 20/20 opening rays clear, evaluated triangle counts below 100,000, ceiling/wall overlap 0.01 m after correction, and tin/table contact within 2.5 mm. This limited audit does not establish full prop BVH clearance, final artistic approval or runtime performance. Source ZIP includes all five updated Blender scenes and forty matching renders.

## Revision 0.4 — four languages and side dossiers

- 28 existing unit tests pass.
- `tools/check_four_languages.py` passes: all 373 catalog strings per new language present, main campaign completed in vi/en/ja/zh (80 main puzzle submissions), both side dossiers completed in each language (24 side puzzle submissions), incorrect answers preserve progress, and save/load preserves side-story completion.
- Japanese and Simplified Chinese use offline Argos model drafts. Completeness and rendered glyphs do not establish translation accuracy; native-speaker review remains required.
- Noto Sans CJK is bundled with its license. Japanese and Chinese chapter screenshots were inspected.
- Two side dossiers add six puzzles. They are optional document investigations, not additional 3D levels. The main campaign remains five short chapters. The requested 4–6 hours has not been achieved or measured.
- No new Windows or UHD 620 acceptance is claimed. Existing Blender Form sources remain unintegrated.

UI review caught literal translations of “tin” and incorrect Japanese action labels. `tools/curate_localization.py` supplies authored Japanese/Chinese interface overrides and corrected biscuit-tin prompts; regeneration reapplies them. Narrative translations remain draft quality.
