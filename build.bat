@echo off

color b

REM Attempt to run pyinstaller build command
pyinstaller.exe --noupx --onefile --add-data "assets/;assets" --hidden-import=PIL --hidden-import=pystray --hidden-import=keyboard  --icon=assets/icon.ico main.pyw

REM Check if the previous command failed due to pyinstaller not being installed
if %errorlevel% equ 9009 goto pyinstaller

REM Build successful
echo Build successful.
goto end

:pyinstaller
echo PyInstaller not found, attempting to install...
pip install pyinstaller
if %errorlevel% neq 0 (
  REM Installation failed
  echo PyInstaller installation failed. Please install manually and try again.
  goto end
)

REM Installation successful, retrying build
echo PyInstaller installed successfully.
echo Retrying pyinstaller build command...
pyinstaller.exe --noupx --onefile --add-data "assets/;assets" --hidden-import=PIL --hidden-import=pystray --hidden-import=keyboard  --icon=assets/icon.ico main.pyw

REM Check if build failed again
if %errorlevel% neq 0 (
  echo Build failed again. Try again or create an issue on the github.
  goto end
)

REM Build successful after installing PyInstaller
echo Build successful.
pause

:end
color f
pause
