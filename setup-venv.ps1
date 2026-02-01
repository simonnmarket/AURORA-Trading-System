# PowerShell script to create and activate a Python 3.11 virtual environment and install requirements.

# Define the name of the virtual environment
$venvName = "venv"

# Create the virtual environment
python3.11 -m venv $venvName

# Activate the virtual environment
.\\$venvName\Scripts\Activate.ps1

# Install the required packages
pip install -r requirements.txt
