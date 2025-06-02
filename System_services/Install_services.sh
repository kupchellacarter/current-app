#!/bin/bash

set -e

# Define paths
SERVICE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SYSTEMD_DIR="/etc/systemd/system"

echo "Copying service files to $SYSTEMD_DIR..."

# Copy each service
sudo cp "$SERVICE_DIR/canup.service" "$SYSTEMD_DIR/"
sudo cp "$SERVICE_DIR/gui.service" "$SYSTEMD_DIR/"

# Reload systemd to recognize new files
echo "Reloading systemd..."
sudo systemctl daemon-reload

# Enable services
echo "Enabling services to run on boot..."
sudo systemctl enable canup.service
sudo systemctl enable gui.service

echo "Done. You can now reboot or run:"
echo "  sudo systemctl start canup.service"
echo "  sudo systemctl start gui.service"
