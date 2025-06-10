#!/bin/bash

# Digital Gauge Cluster Install Script
set -e

echo "🔧 Updating system..."
sudo apt update
sudo apt upgrade -y

echo "📦 Installing dependencies..."
sudo apt install -y python3 python3-pip python3-dev python3-kivy python3-setuptools git i2c-tools python3-smbus   libatlas-base-dev python3-numpy python3-can screen overlayroot

echo "📦 Installing Python packages..."
pip3 install adafruit-circuitpython-dht RPI.GPIO spidev

echo "📁 Enabling I2C and SPI interfaces..."
sudo raspi-config nonint do_i2c 0
sudo raspi-config nonint do_spi 0

echo "🛠️ Configuring OverlayFS support..."
sudo cp /etc/overlayroot.conf /etc/overlayroot.conf.bak || true
echo "overlayroot=tmpfs" | sudo tee /etc/overlayroot.conf > /dev/null

echo "📁 Creating persistent layout config directory..."
sudo mkdir -p /boot/layout_config
sudo chmod 777 /boot/layout_config

echo "🧹 Cleaning up Python cache files..."
find . -name "__pycache__" -type d -exec rm -r {} +

echo "✅ Install complete. Reboot now? (y/n)"
read confirm && if [[ "$confirm" =~ ^[Yy]$ ]]; then sudo reboot; fi
