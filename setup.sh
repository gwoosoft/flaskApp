#!/bin/bash
# Create a symlink in ~/bin (or any folder in PATH)
mkdir -p ~/bin
ln -sf "$(pwd)/flaskdev.sh" ~/bin/flaskdev
echo "flaskdev command is ready. Run 'flaskdev' from anywhere."
