#!/bin/bash

echo "🚀 Starting Digital Cluster Install Script..."

# Ensure python3 and pip are installed
sudo apt update
sudo apt install -y python3 python3-pip git i2c-tools

# Optional: install system packages for I2C, CAN, and DHT
sudo apt install -y python3-smbus python3-dev python3-spidev python3-serial

# Install pip requirements if requirements.txt exists
if [ -f "requirements.txt" ]; then
    pip3 install -r requirements.txt
fi

# Enable I2C and SPI
sudo raspi-config nonint do_i2c 0
sudo raspi-config nonint do_spi 0

# Create project directories
echo "🔧 Setting up file structure..."
mkdir -p config/layout_profiles
mkdir -p logs/can_logs
mkdir -p logs/dtc_snapshots
mkdir -p logs/debug
mkdir -p services
touch logs/alert_log.txt

# Copy and enable services
echo "📦 Installing systemd services..."
sudo cp services/gauge_cluster.service /etc/systemd/system/
sudo cp services/brightness_control.service /etc/systemd/system/
sudo cp services/ups_monitor.service /etc/systemd/system/
sudo systemctl daemon-reexec
sudo systemctl enable gauge_cluster.service
sudo systemctl enable brightness_control.service
sudo systemctl enable ups_monitor.service

echo "✅ Install complete. Reboot recommended."
