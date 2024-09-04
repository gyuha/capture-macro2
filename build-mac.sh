#!/bin/zsh
#pyinstaller --name=CaptureMacro --windowed --onefile --icon="resources/icon.png" --add-data "resources:resources" app.py
#pyinstaller --name=CaptureMacro --windowed --onefile --icon="resources/icon.png" --add-data "resources:resources" app.py
pyinstaller --name=CaptureMacro --onefile --icon="resources/icon.png" --add-data "resources:." app.py
