#!/bin/bash

# This script assumes you're inside the cloned Digital-cluster directory
echo "📂 Organizing Digital-cluster project files..."

# Create folders
mkdir -p services config/layout_profiles logs/can_logs logs/dtc_snapshots logs/debug

# Move service files
mv gauge_cluster.service services/ 2>/dev/null
mv brightness_control.service services/ 2>/dev/null
mv ups_monitor.service services/ 2>/dev/null

# Move config files
mv default_theme.json config/ 2>/dev/null
mv default_pid_mappings.json config/ 2>/dev/null

# Optionally move layout profiles
mv *.layout.json config/layout_profiles/ 2>/dev/null

# Move logs if present
mv *.log logs/ 2>/dev/null

echo "✅ File organization complete. Ready to commit and push."
