@echo off
cd /d "%~dp0"
python -m netboost
if errorlevel 1 py -m netboost
echo If the window did not open, go to http://127.0.0.1:8765
pause
