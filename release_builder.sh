#!/bin/sh

# Clean the release dir
rm -rf release/*
# Copy the source and license file
mkdir -p release/ResistorDecoder/ResistorDecoder
cp -a src/* release/ResistorDecoder/ResistorDecoder
cp LICENSE release/ResistorDecoder
cp setup.py release/ResistorDecoder
cp README.md release/ResistorDecoder
cp dist/ResistorDecoder.desktop release/ResistorDecoder
cp icons/resistor_decoder.png release/ResistorDecoder
# Delete the pycache
cd release
find . -type d -name __pycache__ -exec rm -dr {} \;
# Add root dependency to all imports
find . -exec sed -i "s/from src./from ResistorDecoder./g;
                     s/import src./import ResistorDecoder./g;
                     s/import resource_base_rc/import ResistorDecoder.resource_base_rc/g;
                     s/from ui_generated_files/from ResistorDecoder.ui_generated_files/g" {} \;
# Create the tarball
tar -czf ResistorDecoder-1.0.tar.gz ResistorDecoder