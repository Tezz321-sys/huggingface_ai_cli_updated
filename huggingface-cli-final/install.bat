@echo off
echo Installing AI CLI OS-Independent...
pip install -r requirements.txt --break-system-packages
pip install -e . --break-system-packages
echo Installation complete! Try running: ai --help
pause
