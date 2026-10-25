"""Build a Windows standalone folder; must run on Windows."""
import platform,subprocess,sys,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
if platform.system()!='Windows':raise SystemExit('Windows packaging must run on Windows. No EXE was produced.')
subprocess.run([sys.executable,'-m','PyInstaller','--noconfirm','--clean','--windowed','--onedir','--name','Game','--collect-all','panda3d','--collect-all','direct','--add-data',f'{ROOT / "assets"};assets','--add-data',f'{ROOT / "data"};data',str(ROOT/'run_game.py')],cwd=ROOT,check=True)
release=ROOT/'dist/Game'
for name in ['README.md','LICENSE','BUILD_INSTRUCTIONS.md','TEST_REPORT.md']:shutil.copy2(ROOT/name,release/name)
subprocess.run([sys.executable,str(ROOT/'tools/verify_release.py'),str(release)],check=True)
shutil.make_archive(str(ROOT/'dist/Game_Release_Windows'),'zip',release)
print('Packaged dist/Game_Release_Windows.zip. Launch Game.exe manually for Windows acceptance testing.')
