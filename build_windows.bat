@echo off
pyinstaller --onefile --noconsole easypie_pyinstaller.spec --distpath dist\windows
echo y | mkdir dist\windows\demo_projects 
xcopy demo_projects dist\windows\demo_projects\ /s/h/e/k/f/c/y
rmdir /s /q build
