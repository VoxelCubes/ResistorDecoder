#!/bin/sh

# Clean the release dir
rm -rf release/*
# Copy the source and license file
mkdir -p release/ResistorDecoder/ResistorDecoder
cp -a ResistorDecoder/src release/ResistorDecoder/ResistorDecoder
cp LICENSE release/ResistorDecoder
cp setup.py release/ResistorDecoder
cp README.md release/ResistorDecoder
cp dist/ResistorDecoder.desktop release/ResistorDecoder
cp ResistorDecoder/icons/resistor_decoder.png release/ResistorDecoder
touch release/ResistorDecoder/ResistorDecoder/__init__.py
# Delete the pycache
cd release
find . -type d -name __pycache__ -exec rm -dr {} \;
# Add root dependency to all imports
find . -exec sed -i "s/import resource_base_rc/import ResistorDecoder.src.resource_base_rc/g" {} \;
# Create the tarball
tar -czf ResistorDecoder-1.0.tar.gz ResistorDecoder