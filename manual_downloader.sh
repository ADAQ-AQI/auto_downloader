#!/bin/bash

## Check that geckodriver path is set, and add to PATH if not already done:
if [ -f "/home/h06/cbosley/geckodriver_box" ]; then
        . "/home/h06/cbosley/geckodriver_box"
else
    export PATH="/home/h06/cbosley/geckodriver_box:$PATH"
fi

## Add a conda executable to user's PATH, allowing Elle to use a temporary conda env containing selenium.
if [ -f "/data/users/cbosley/conda/bin" ]; then
        . "/data/users/cbosley/conda/bin"
else
    export PATH="/data/users/cbosley/conda/bin:$PATH"
fi

# Create directory for confirmation pages:
rm -rf confirmations
mkdir -p confirmations

# Activate selenium environment and run script, then deactivate environment:
source activate
python manual_downloader.py
source deactivate

