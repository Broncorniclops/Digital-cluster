#!/bin/bash
# This script creates a persistent layout config directory on the /boot partition
# and updates permissions so your gauge cluster can write to it.

set -e

# Step 1: Create layout_config folder if it doesn't exist
if [ ! -d /boot/layout_config ]; then
    echo "Creating /boot/layout_config..."
    sudo mkdir /boot/layout_config
    sudo chmod 777 /boot/layout_config
    echo "✓ Directory created."
else
    echo "✓ /boot/layout_config already exists."
fi

# Step 2: Test write access
echo "Testing write access..."
echo "{\"layout\":\"test\"}" > /boot/layout_config/test_write.json
if [ -f /boot/layout_config/test_write.json ]; then
    echo "✓ Write test passed. Persistent path is ready."
    rm /boot/layout_config/test_write.json
else
    echo "✗ Write test failed. Check permissions."
fi
