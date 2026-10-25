@echo off
setlocal
cd /d "%~dp0\.."
where py >nul 2>nul
if errorlevel 1 (
 echo Install Python 3.12 64-bit from python.org on the build machine.
 exit /b 1
)
if not exist .venv\Scripts\python.exe py -3.12 -m venv .venv
if errorlevel 1 exit /b 1
.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
if errorlevel 1 exit /b 1
.venv\Scripts\python.exe -m pytest -q
if errorlevel 1 exit /b 1
.venv\Scripts\python.exe tools\build.py
exit /b %errorlevel%
