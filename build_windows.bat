@echo off
setlocal
cd /d "%~dp0"
py -3.12 -m venv .venv
if errorlevel 1 exit /b 1
call .venv\Scripts\activate.bat
python -m pip install -r requirements-dev.txt
if errorlevel 1 exit /b 1
python tools\validate_content.py
if errorlevel 1 exit /b 1
python -m pytest -q
if errorlevel 1 exit /b 1
python -m PyInstaller --noconfirm --clean --windowed --name 3DPsychocal --icon assets\ui\icon.ico --add-data "assets;assets" --add-data "data;data" main.py
if errorlevel 1 exit /b 1
powershell -NoProfile -Command "$p = Start-Process -FilePath '.\dist\3DPsychocal\3DPsychocal.exe' -ArgumentList '--headless','--frames','30','--user-dir','work\exe-smoke' -Wait -PassThru; exit $p.ExitCode"
if errorlevel 1 exit /b 1
powershell -NoProfile -Command "Compress-Archive -Path dist\3DPsychocal -DestinationPath dist\3DPsychocal-Windows.zip -Force"
echo Build complete: dist\3DPsychocal-Windows.zip
endlocal
