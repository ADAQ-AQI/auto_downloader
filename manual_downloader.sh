#!/bin/bash

## Check that geckodriver path is set, and add to PATH if not already done:
if [ -f "/home/h06/cbosley/geckodriver_box" ]; then
        . "/home/h06/cbosley/geckodriver_box"
else
    export PATH="/home/h06/cbosley/geckodriver_box:$PATH"
fi


#TODO: Find or create tmp directory for downloads
#TODO: add environment to path and activate it

python manual_downloader.py

# TODO: deactivate environment
