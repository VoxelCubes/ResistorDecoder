##!/bin/python
import os

"""
python -m nuitka --help
# Windows:
python -m nuitka --onefile --plugin-enable=pyside6 -o "ResistorDecoder.exe" --windows-disable-console --windows-icon-from-ico=icons\resistor_decoder.png --output-dir=nuitka_build src\main.py
# Linux:
python -m nuitka --onefile --plugin-enable=pyside6 -o "ResistorDecoder-1.0.appimage" --windows-disable-console --linux-onefile-icon=icons/resistor_decoder.png --output-dir=nuitka_build src/main.py
"""

# QT plugins are copied from the site-packages folder into .\qtplugins\ for the pyinstaller build.
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = "."  #"qtplugins"

import sys
import PySide6.QtWidgets as Qw
import PySide6.QtCore as Qc
from src.driver_resistance_calc import ResistanceCalc



def main():
    Qw.QApplication.setAttribute(Qc.Qt.AA_EnableHighDpiScaling, True)
    Qw.QApplication.setAttribute(Qc.Qt.AA_UseHighDpiPixmaps, True)

    app = Qw.QApplication(sys.argv)

    window = ResistanceCalc()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
