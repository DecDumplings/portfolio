@echo off
echo Updating Portfolio Assets...
python update_gallery.py
echo.
echo Starting Local Server...
echo Please ensure you allow Python access if prompted by Firewall.
echo The browser will open shortly.
start http://localhost:8000
python -m http.server 8000
pause
