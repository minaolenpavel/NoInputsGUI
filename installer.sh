#!/bin/bash

set -e

APP_NAME="noinputs-gui"
INSTALL_DIR="/usr/local/bin"

echo "Installing $APP_NAME..."

sudo cp dist/$APP_NAME $INSTALL_DIR/
sudo chmod +x $INSTALL_DIR/$APP_NAME

# Install udev rules
echo "Installing udev rules..."
sudo cp ./rules/99-noinputs.rules /etc/udev/rules.d/

# Reload udev
sudo udevadm control --reload-rules
sudo udevadm trigger

# Create group and add user
sudo groupadd -f noinputs
sudo usermod -a -G noinputs $USER

echo "Done. Please logout and login for group permissions to take effect."