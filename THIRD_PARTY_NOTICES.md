# Third-party notices

- Project code, story, generated geometry, six textures and five WAVs are provided under this repository's Apache License 2.0. Asset generation uses deterministic algorithms in tools/generate_assets.py; no external commercial game assets or music were used.
- DejaVu Sans is bundled. Its copyright and license are included at assets/fonts/LICENSE-DejaVu.txt; font distribution terms are separate from the project license.
- Panda3D 1.10.16: BSD-style license; https://github.com/panda3d/panda3d/blob/v1.10.16/LICENSE. Panda3D also includes third-party components; preserve its dependency notices when distributing binary builds.
- Pillow 11.3.0: HPND/PIL license; https://github.com/python-pillow/Pillow/blob/11.3.0/LICENSE. Used by the offline asset generator.
- PyInstaller 6.16.0: GPL with bootloader exception permitting distribution of applications under their own terms; https://pyinstaller.org/en/stable/license.html.
- Python runtime: PSF license; https://docs.python.org/3/license.html. pytest and its dependencies are development-only.

The Windows build collects Panda3D/direct package data and distribution metadata. Review the generated binary distribution and its bundled notices before a public release.

Noto Sans CJK is bundled under its own font license, reproduced in assets/fonts/LICENSE-NotoCJK.txt. Japanese/Chinese drafts were produced offline with Argos Translate models (en-ja 1.1, en-zh 1.9) and CTranslate2; model weights are authoring dependencies and are not shipped or required at runtime.
