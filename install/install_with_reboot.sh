#!/bin/bash
echo "[INFO] Running initial install..."
sudo apt-get update
sudo apt-get install -y python3 python3-pip i2c-tools can-utils git
sudo pip3 install -r requirements.txt

# Enable I2C and SPI if not already enabled
sudo raspi-config nonint do_i2c 0
sudo raspi-config nonint do_spi 0

# Enable services
sudo systemctl enable gauge_cluster.service
sudo systemctl enable ups_monitor.service
sudo systemctl enable brightness_control.service

# Set executable permissions
chmod +x install/first_boot_config.sh
chmod +x install/system_paths_setup.sh

# Run setup
install/first_boot_config.sh
install/system_paths_setup.sh

echo "[INFO] Setup complete. Rebooting..."
sudo reboot