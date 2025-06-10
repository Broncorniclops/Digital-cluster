#!/bin/bash

echo "Installing Python dependencies from requirements.txt..."
if [ -f requirements.txt ]; then
    pip3 install -r requirements.txt
else
    echo "Error: requirements.txt not found in the current directory."
    exit 1
fi