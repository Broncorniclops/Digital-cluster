#!/bin/bash
# First Boot Configuration Script for Digital Cluster

LOGFILE="/var/log/first_boot_config.log"
exec > >(tee -a $LOGFILE) 2>&1

echo "Starting first boot configuration..."

# Update system and install essential packages
apt-get update && apt-get upgrade -y
apt-get install -y git i2c-tools python3-pip python3-smbus python3-dev libffi-dev libssl-dev build-essential

# Enable I2C and SPI
raspi-config nonint do_i2c 0
raspi-config nonint do_spi 0

# Set up hostname
echo "digital-cluster" > /etc/hostname
sed -i 's/127.0.1.1.*/127.0.1.1\tdigital-cluster/' /etc/hosts

# Set up I2C permissions
adduser pi i2c

# Set default timezone
timedatectl set-timezone America/Chicago

# Install Python packages
pip3 install --upgrade pip
pip3 install kivy RPi.GPIO adafruit-circuitpython-dht adafruit-blinka adafruit-circuitpython-tsl2591 smbus2 numpy

# Clone GitHub repository if not already cloned
REPO_DIR="/home/pi/Digital-cluster"
if [ ! -d "$REPO_DIR" ]; then
  git clone https://github.com/Broncorniclops/Digital-cluster.git $REPO_DIR
  chown -R pi:pi $REPO_DIR
fi

# Move config files into place
cp $REPO_DIR/install/wpa_supplicant.conf /etc/wpa_supplicant/wpa_supplicant.conf
chmod 600 /etc/wpa_supplicant/wpa_supplicant.conf

# Enable required services
systemctl enable gauge_cluster.service
systemctl enable brightness_control.service
systemctl enable ups_monitor.service

# Reboot to apply changes
echo "First boot setup complete. Rebooting..."
reboot
