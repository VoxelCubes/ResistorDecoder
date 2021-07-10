#!/bin/sh

# Copy the source and license files
cp -a src/ release/ResistorDecoder/ 
cp -a LICENSE release/ResistorDecoder
# Delete the pycache
cd release
find . -type d -name __pycache__ -exec rm -dr {} \;
# Create the tarball
tar -czf ResistorDecoder-1.0.tar.gz ResistorDecoder