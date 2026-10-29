@echo off
setlocal
cd /d "%~dp0"
python -m pip install -r ebook\requirements.txt pyinstaller
if errorlevel 1 exit /b 1
pushd ebook\frontend
call npm ci
if errorlevel 1 exit /b 1
call npm run build
if errorlevel 1 exit /b 1
popd
python -m PyInstaller --noconfirm --onefile --windowed --name eBook-studio --paths . --icon ebook\assets\app.ico --add-data "ebook/assets;ebook/assets" --add-data "ebook/frontend/dist;ebook/frontend/dist" ebook\desktop.py
exit /b %errorlevel%
