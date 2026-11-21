@echo off
chcp 65001 >nul
echo === Instalujem potrebne kniznice ===
python -m pip install --upgrade pip
python -m pip install matplotlib pyinstaller
echo.
echo === Vytvaram .exe subor ===
python -m PyInstaller --onefile --windowed --clean --name AnalyzaMeranychHodnot aplikacia.py
echo.
echo Hotovo! Subor najdete v: dist\AnalyzaMeranychHodnot.exe
pause
