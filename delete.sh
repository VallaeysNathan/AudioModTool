#!/bin/bash

# --------------------------
# Config
# --------------------------
TOOL_NAME="AudioModTools"
VENV_DIR="$HOME/.audiomodtools_venv"
WRAPPER="$HOME/bin/$TOOL_NAME"

# --------------------------
# Remove wrapper
# --------------------------
if [ -f "$WRAPPER" ]; then
    rm "$WRAPPER"
    echo "Removed wrapper: $WRAPPER"
else
    echo "Wrapper not found: $WRAPPER"
fi

# --------------------------
# Remove virtual environment
# --------------------------
if [ -d "$VENV_DIR" ]; then
    rm -rf "$VENV_DIR"
    echo "Removed virtual environment: $VENV_DIR"
else
    echo "Virtual environment not found: $VENV_DIR"
fi

# --------------------------
# Remove PATH modification from ~/.bashrc
# --------------------------
if grep -q 'export PATH="$HOME/bin:$PATH"' "$HOME/.bashrc"; then
    # Remove the line
    sed -i '/export PATH="\$HOME\/bin:\$PATH"/d' "$HOME/.bashrc"
    echo "Removed PATH modification from ~/.bashrc"
else
    echo "No PATH modification found in ~/.bashrc"
fi

echo "Uninstallation complete!"
echo "You may want to reload your shell:"
echo "  source ~/.bashrc"
