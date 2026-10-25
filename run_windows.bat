@echo off
setlocal
cd /d "%~dp0"
if exist .venv\Scripts\python.exe goto run
py -3.12 -m venv .venv
if errorlevel 1 exit /b 1
.venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 exit /b 1
:run
.venv\Scripts\python.exe main.py
endlocal
