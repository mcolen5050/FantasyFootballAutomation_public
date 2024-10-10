#!/bin/bash

# Create a virtual environment
python3 -m venv fantasy_env

# Activate the virtual environment
source fantasy_env/bin/activate

# Install the required dependencies directly
pip install selenium webdriver_manager espn_api

echo "Setup complete! Your virtual environment is activated and dependencies are installed."
