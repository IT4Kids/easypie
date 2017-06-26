pyinstaller --onefile --noconsole easypie_pyinstaller.spec --distpath dist/linux
xcopy examples dist/windows/ /E /H
rmdir /s build
cd dist/linux