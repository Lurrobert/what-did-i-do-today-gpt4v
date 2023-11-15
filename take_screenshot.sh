#!/bin/bash
# replace with your folder!
screenshot_path="YOURFOLDER/screenshots/Screenshot_$(date +\%Y\%m\%d\%H\%M\%S).png"

# Capture the screenshot without any quality drop
/usr/sbin/screencapture -x "$screenshot_path"

# Resize the image to make it a little smaller
sips -Z 1530 "$screenshot_path"