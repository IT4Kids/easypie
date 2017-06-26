@echo off
REM This script requires a very recent version of PyInstaller due to changes in PyQt5 structure.
REM See: https://github.com/pyinstaller/pyinstaller/pull/2403, applying it will fix build issues such as PyQt5.dll not found.
REM All warnings that include the windows-crt may be safely ignored.
pyinstaller --onefile --noconsole easypie_pyinstaller.spec --distpath dist\windows
echo y | mkdir dist\windows\demo_projects 
xcopy demo_projects dist\windows\demo_projects\ /s/h/e/k/f/c/y
rmdir /s /q build
