# Build instructions / Hướng dẫn build

## Windows 10/11 x64 (build host)

1. Install Python **3.12 x64** from python.org with the `py` launcher.
2. Extract the source archive. Double-click `tools\build_windows.bat` or run it from a terminal.
3. The script creates `.venv`, installs pinned dependencies, runs the logic tests, and uses PyInstaller to build `dist\Game\Game.exe` with assets and DLLs in `_internal`.
4. It verifies the PE signature and required resource files, then creates `dist\Game_Release_Windows.zip`.
5. **Acceptance test required:** unzip to another path (including a path with spaces and Vietnamese characters), disconnect the network and launch `Game.exe`. Play both languages, finish each chapter, save/restart/load, test all endings and audio. Test on a clean Windows machine without Python. Do not ship only the EXE: distribute the whole ZIP/folder.

The build script has been authored but **has not been run on Windows**. The current development machine is Linux; no Windows release ZIP or EXE is claimed or supplied. `tools/build.py` rejects non-Windows hosts instead of producing a mislabeled binary. Dependencies may need Internet at build time; the resulting game uses no network at runtime.

## Linux development and checks

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
.venv/bin/python -m pytest -q
.venv/bin/python run_game.py
```

Desktop play requires a graphical display and OpenGL. Headless rendering on Mesa/EGL:

```sh
EGL_PLATFORM=surfaceless XDG_CACHE_HOME=/tmp/game-cache .venv/bin/python run_game.py --smoke --screenshot /tmp/game.png
EGL_PLATFORM=surfaceless XDG_CACHE_HOME=/tmp/game-cache .venv/bin/python tools/render_validation.py /tmp/game-validation
```

Offscreen checks use a null audio backend and temporary save directories. They do not test physical mouse capture, speakers, fullscreen transitions or Windows compatibility.

## Rebuild source archive

Run `python tools/package_source.py`. It includes source, story, assets, tests, licenses, documentation and build tools, excluding environments, caches, Git history and output archives. Asset locations are resolved from the source root or PyInstaller bundle, never the current working directory. Save data is stored outside the installation folder.

## Optional GitHub Actions build

The repository includes `.github/workflows/windows-build.yml`. After committing/pushing the project, run **Build Windows development package** manually in Actions. It builds on Windows and uploads the player ZIP if packaging succeeds. This workflow has not been executed in this session and does not replace clean-machine playtesting. No push or external CI run was performed here.

## Blender design proposals

`blender --background --python tools/design_rooms_blender.py` reproduces the five Function-review `.blend` files and 20 renders. These are design proposals, not final approved runtime scenes. `tools/prepare_room_review.py` uses included templates; rerunning intentionally resets approvals. The plugin’s opening tracer additionally requires OpenCV, and its validator comes from the installed Build 3D Game Rooms skill. Those authoring dependencies are separate from the game runtime.
