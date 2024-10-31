#!/bin/bash

# Variables (update these to match your setup)
SERVICE_NAME="ocr_service"
WORKING_DIR="/opt/ocr_service"
PYTHON_PATH="/usr/bin/python3"  # Path to the Python interpreter
SCRIPT_PATH="$WORKING_DIR/main.py"  # Path to your main script
SERVICE_FILE="/etc/systemd/system/$SERVICE_NAME.service"

# Define the service content
SERVICE_CONTENT="[Unit]
Description=OCR Flask Service
After=network.target

[Service]
ExecStart=$WORKING_DIR/venv/bin/python $SCRIPT_PATH
WorkingDirectory=$WORKING_DIR
Restart=always
User=pi
Environment=PATH=$WORKING_DIR/venv/bin:$PATH

[Install]
WantedBy=multi-user.target
"

# Install necessary packages
echo "Updating package list and installing required packages..."
sudo apt-get update -y
sudo apt-get install -y python3 python3-pip python3-venv tesseract-ocr

# Set up virtual environment and install Python dependencies
echo "Setting up virtual environment and installing Python dependencies..."
mkdir -p $WORKING_DIR
python3 -m venv $WORKING_DIR/venv
source $WORKING_DIR/venv/bin/activate
pip install flask pillow pytesseract

# Write the systemd service file
echo "Creating systemd service file..."
echo "$SERVICE_CONTENT" | sudo tee $SERVICE_FILE

# Reload systemd to recognize the new service, enable, and start it
echo "Enabling and starting the service..."
sudo systemctl daemon-reload
sudo systemctl enable $SERVICE_NAME
sudo systemctl start $SERVICE_NAME

# Notify the user
echo "Service $SERVICE_NAME has been installed, enabled, and started successfully."
