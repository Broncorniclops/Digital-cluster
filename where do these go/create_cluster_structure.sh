#!/bin/bash

echo "🔧 Creating Digital-cluster directory structure..."

BASE_DIR="/home/pi/Digital-cluster"

# Core folders
mkdir -p "$BASE_DIR"
mkdir -p "$BASE_DIR/config/layout_profiles"
mkdir -p "$BASE_DIR/logs/can_logs"
mkdir -p "$BASE_DIR/logs/dtc_snapshots"
mkdir -p "$BASE_DIR/logs/debug"
mkdir -p "$BASE_DIR/services"

# Touch base log file
touch "$BASE_DIR/logs/alert_log.txt"

echo "✅ Directory structure created successfully."
