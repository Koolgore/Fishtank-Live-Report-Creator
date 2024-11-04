#!/bin/bash
echo "Upgrading pip..."
python3 -m pip install --upgrade pip

echo "Installing dependencies from requirements.txt..."
python3 -m pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "All dependencies have been successfully installed."
else
    echo "An error occurred while installing dependencies."
fi
