#!/bin/bash

# Check if pip exists
if ! command -v pip &> /dev/null
then
    echo "pip could not be found. Installing..."

    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python get-pip.py
    rm get-pip.py

    echo "pip installed successfully."
else
    echo "pip is already installed."
fi

echo "check requirements..."

pip install --root-user-action=ignore -r requirements -q

echo "continue."

python bot.py
