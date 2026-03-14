#!/bin/bash
set -e

APP_NAME="noinputs"
APP_PATH="$1"

echo "Installing $APP_NAME..."

# Copy udev rules
cp "$APP_PATH"/rules/99-noinputs.rules /etc/udev/rules.d/
udevadm control --reload-rules
udevadm trigger
echo "udev rules installed"

# Create group and add user
groupadd -f noinputs
usermod -aG noinputs $USER
echo "Added $USER to 'noinputs' group. Please restart for changes to take effect."