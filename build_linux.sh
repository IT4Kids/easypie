#!/usr/bin/env bash
pyinstaller --onefile --noconsole easypie_pyinstaller.spec --distpath dist/linux
cp -r examples dist/linux/
rm -r build
cd dist/linux
zip easypie_linux_0_1_0.zip -r .
