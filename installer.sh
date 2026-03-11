#!/bin/bash
set -e

APP_NAME="noinputs"
INSTALL_DIR="/usr/bin"

echo "Installing $APP_NAME..."

# Make sure the binary exists
if [ ! -f "dist/$APP_NAME" ]; then
    echo "Error: $APP_NAME binary not found in dist/"
    exit 1
fi

# Copy binary to /usr/bin
sudo cp dist/$APP_NAME $INSTALL_DIR/
sudo chmod +x $INSTALL_DIR/$APP_NAME
echo "$APP_NAME installed to $INSTALL_DIR"

# Copy udev rules
sudo cp rules/99-noinputs.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules
sudo udevadm trigger
echo "udev rules installed"

# Create group and add user
sudo groupadd -f noinputs
sudo usermod -aG noinputs $USER
echo "Added $USER to 'noinputs' group. Please logout/login for group changes to take effect."