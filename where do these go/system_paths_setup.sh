#!/bin/bash
echo "[INFO] Setting up required system paths..."

mkdir -p /home/pi/cluster/data
mkdir -p /home/pi/cluster/data/can_logs
mkdir -p /home/pi/cluster/data/dtc_snapshots
mkdir -p /home/pi/cluster/data/error_logs
mkdir -p /home/pi/cluster/config/user_profiles

touch /home/pi/cluster/data/alert_log.txt

echo "[INFO] Paths created and initialized."
