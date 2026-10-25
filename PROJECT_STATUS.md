# Bến Không Tên — noncommercial development project

This repository contains an unfinished game. It must not be described as a finished 4–6 hour release.

Current implementation: five short main chapters, twenty deductions, three endings, fifteen extended conversation topics, two optional dossier side stories with six additional puzzles, four selectable languages, inventory/evidence inspection, linked evidence, save slots/backups and chapter replay. Side stories are text-based dossier investigations; they are not two new 3D maps.

Vietnamese and English are authored. Japanese and Simplified Chinese use complete offline draft translation catalogs generated with official Argos models through CTranslate2. They require native-speaker editorial review; translation coverage and rendering are checked separately from linguistic quality. Noto CJK and its license are bundled. Gameplay does not require a translation model or network.

Five more detailed Blender scene sources and forty review images are present. They remain awaiting Form approval and runtime integration; the current playable scenes are still procedural development environments. More locations, detailed character art, substantially expanded branching content and meaningful timed playtests are required for the requested scope.

Windows packaging tools and a manually triggered GitHub Actions workflow are included. No Windows runtime acceptance or target Intel UHD 620 performance claim is made. The existing Apache-2.0 license is retained; the project's noncommercial development intent does not revoke that license's permissions.

Use GitHub's **Code → Download ZIP** on the development branch to obtain the complete committed project. `python tools/package_source.py` produces a verified local archive with SHA-256 hashes. Repository archives do not include a fabricated Game.exe.
