#!/bin/bash
# Setup script for Raspberry Pi OS Lite (64-bit) - Digital Gauge Cluster

echo "Updating system..."
sudo apt update && sudo apt upgrade -y

echo "Installing core packages..."
sudo apt install -y python3-pip git python3-dev libatlas-base-dev libffi-dev libjpeg-dev libSDL2-dev libmtdev-dev libgl1-mesa-dev libgles2-mesa-dev libgstreamer1.0-dev gstreamer1.0-plugins-base gstreamer1.0-plugins-good libinput-dev libudev-dev xinput evtest

echo "Enabling SPI and I2C interfaces..."
sudo raspi-config nonint do_spi 0
sudo raspi-config nonint do_i2c 0

echo "Installing Kivy for touchscreen UI..."
pip3 install --upgrade pip setuptools wheel
pip3 install kivy[base] kivy_examples

echo "Cloning your digital gauge cluster project..."
cd ~
git clone https://github.com/yourusername/digital_gauge_cluster.git  # Replace with your repo if hosted
cd digital_gauge_cluster

echo "Setup complete. To run the dashboard:"
echo "  cd ~/digital_gauge_cluster"
echo "  python3 main.py"
