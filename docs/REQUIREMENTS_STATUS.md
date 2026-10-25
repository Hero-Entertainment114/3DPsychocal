# Requirements reconciliation — development 0.3

This is a factual acceptance checklist, not a declaration that the master brief is complete.

| Requested outcome | Actual status / evidence |
|---|---|
| Finished 4–6 hour game | **Not achieved or measured.** Current campaign remains short. No waiting gates, slow walking or repetitive filler added to fabricate duration. |
| Five chapters and an ending | Implemented and executed in two languages; five current procedural scenes, four deductions each. |
| 15–20 independent puzzles | 20 authored prompts with solutions, prerequisites, two hints, incorrect-answer recovery. Five use ordering cards; others use codes or choices. More tactile environmental variety still needed. |
| Three major twists | Implemented in the short script: contradictory memory, rescued family, mother's role. Long-form pacing and outside editorial review pending. |
| Three genuinely different endings | Implemented and triggered in tests; cooperative route requires witness consent. |
| 6–10 meaningful characters | Six interactable in-world characters; additional cast in documents. Longer dialogue trees, schedules, rigs and sophisticated animation not complete. |
| Vietnamese and English | Both supported for UI, story, documents, hints, endings, new settings and inspection. Default Vietnamese; font included; rendered text checked. |
| Walking, running, crouch, camera | Implemented; simulated movement and rebound-key events tested. Physical desktop mouse capture not tested. |
| Walls and collision | Bounds and furniture collision implemented; target reachability checked. Current scenes still use nontraversable transition-door markers. Proposed Blender replacement has real Boolean openings but is not yet approved/integrated. |
| Pick up, inspect, rotate objects | Evidence collection and rotatable 3D document inspection implemented. Generic paper surface currently reused; not all unique artifact models/artwork finished. |
| Use items, doors, drawers | Biscuit-tin key unlocks the archive drawer, slides it and exposes Mother's draft; saved state restores it. Broader inventory-use system and animated architectural doors not finished. |
| Evidence pinning and connections | Draggable cards, two-card link validation, visual lines, saved pin positions and supported relations implemented. Cross-page selection supported. |
| Dialogue and ethical choices | Text conversations, consent and final disclosure choice implemented. Extended branching confrontations and delayed consequences incomplete. |
| Journal, inventory, map | Implemented; evidence pagination, 3D inspection and area map available. |
| Autosave, three manual slots, backup | Implemented and tested; schema v2 migrates v1 checkpoints; atomically replaces files and falls back to previous healthy copy. |
| Chapter select | Unlocked-chapter replay implemented; tests verify campaign saves remain unchanged. |
| FOV, sensitivity, graphics, resolution, fullscreen | Implemented; graphics presets still mainly viewing distance. Real-device fullscreen and target performance unverified. |
| Rebinding, font size, bob, brightness | Implemented; WASD/interact remapping validates reserved and duplicate keys, input event tested. |
| Audio categories and captions | Music/ambience/effects volumes, ambient-caption toggle implemented. Core story text stays readable, as no voice acting exists. |
| VSync toggle, gamepad | Not implemented. |
| Distinct music | Nine original short synthesized cues plus five existing audio files. File validity and playback routing tested; audible quality not listened to on host. No recorded dialogue. |
| Rich spatial ambient sound | Rain/footsteps/paper/cues available; positional audio, cicadas, traffic, vendor calls and material-specific footsteps incomplete. |
| Five detailed authored rooms | Five distinct Blender Function drafts and 20 views produced. Layout approval received; material/light scenes created, final art/geometry audit and Form approval pending; current playable scenes remain development art. |
| Lux3D and Meshy assets | **No assets generated through these services.** User has no Lux3D account; no service keys/budget present. Lux3D private Python setup works, but its required body.md could not be read. No paid tasks submitted. |
| 30 FPS on UHD 620 | Not tested; no comparable hardware available. |
| Windows standalone EXE | Not built/tested. Windows build script and manually triggered GitHub Actions workflow provided. No fake EXE or player-release ZIP. |
| Complete editable project ZIP | Produced from actual files, including code, assets, tests, documents, Blender drafts and review records. Manifest hashes verify archive contents. |

## Outstanding production and acceptance

The missing content/art cannot be truthfully certified by adding files, raising puzzle counts or running fast automated tests. The 4–6 hour target requires substantially expanded authored scenes, investigations and dialogue, followed by independent timed playthroughs. `State.play_seconds` measures time in active gameplay/narrative panels and excludes the pause menu; it is a measurement tool, not a duration guarantee.

The Meshy-specific validator still fails its service-pricing/budget requirements. Human layout and reference approval has now been received for a local Blender route. `production/room-review/function-validation.txt` records the actual validator results. The five `.blend` files are dimensional Function proposals, not final approved compositions or runtime exports. A local Blender-only route can continue under the received layout/reference approval, but must not be described as a passed Meshy-specific validator route.

## Subsequent approvals and work

The user explicitly approved all five layouts and the tin reference for local Blender construction. This approval does not authorize paid generation, final Form acceptance or runtime deployment. Five material/light Blender scenes and 40 review views have since been built; their current status is recorded in production/form-review/. Fifteen additional authored bilingual conversations are playable. Long-form duration remains unachieved.
