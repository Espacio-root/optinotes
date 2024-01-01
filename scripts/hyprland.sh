#!/bin/bash

# Install required packages
sudo pacman -S --noconfirm --needed python python-pip python-virtualenv

# Create & activate a virtual environment
python3 -m venv ../venv
source ../venv/bin/activate

# Install project dependencies
pip install -r ../requirements.txt

# Deactivate the virtual environment
deactivate

# Install necessary packages
sudo pacman -S --noconfirm --needed grim slurp

# Create a symbolic link to the optinotes script
project_path=$(dirname $(pwd))
echo 'optinotes() {' >> ~/.bashrc
echo "    sudo -E $project_path/venv/bin/python3 $project_path/src/main.py \$*" >> ~/.bashrc
echo '}' >> ~/.bashrc

# Reload .bashrc to apply changes immediately
source ~/.bashrc

echo "Installation complete. You can now use the 'optinotes' command within the virtual environment."
