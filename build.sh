#!/usr/bin/env bash
pyinstaller --onefile --noconsole easypie_pyinstaller.spec
rm -r build
