#!/bin/bash

# --------------------------
# Config
# --------------------------
TOOL_NAME="AudioModTools"
SRC_FILE="main.py"
VENV_DIR="$HOME/.audiomodtools_venv"

# --------------------------
# Check source file
# --------------------------
if [ ! -f "$SRC_FILE" ]; then
    echo "Error: $SRC_FILE not found in current directory."
    exit 1
fi

# --------------------------
# Create virtual environment
# --------------------------
if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
    echo "Created virtual environment at $VENV_DIR"
fi

# Activate venv
source "$VENV_DIR/bin/activate"

# --------------------------
# Install dependencies
# --------------------------
pip install --upgrade pip
pip install numpy scipy

# --------------------------
# Create ~/bin if needed
# --------------------------
mkdir -p "$HOME/bin"

# --------------------------
# Copy tool to ~/bin
# --------------------------
cp "$SRC_FILE" "$HOME/bin/$TOOL_NAME"
chmod +x "$HOME/bin/$TOOL_NAME"

# --------------------------
# Add ~/bin to PATH if missing
# --------------------------
if ! echo "$PATH" | grep -q "$HOME/bin"; then
    echo 'export PATH="$HOME/bin:$PATH"' >> "$HOME/.bashrc"
    echo "Added ~/bin to PATH in ~/.bashrc. Reload your shell or run: source ~/.bashrc"
fi

# Copy Python script into venv
cp "$SRC_FILE" "$VENV_DIR/bin/$SRC_FILE"

# --------------------------
# Create wrapper to run inside venv
# --------------------------
WRAPPER="$HOME/bin/$TOOL_NAME"
cat > "$WRAPPER" << EOF
#!/bin/bash
source "$VENV_DIR/bin/activate"
python "$VENV_DIR/bin/$SRC_FILE" "\$@"
EOF
chmod +x "$WRAPPER"

echo "Installation complete!"
echo "You can now run your CLI tool like this:"
echo "$TOOL_NAME input.wav output.wav -r 16000"
