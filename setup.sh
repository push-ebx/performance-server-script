#!/bin/bash

SCRIPT_DIR=$(dirname "$(realpath "$0")")
SCRIPT_NAME="metrics.py"
CRON_JOB="0 * * * * /usr/bin/python3 /root/performance-server-script/$SCRIPT_NAME >> /var/log/metrics.log 2>&1"

if [ -f "$SCRIPT_DIR/requirements.txt" ]; then
    echo "Installing Python dependencies..."
    sudo pip3 install -r "$SCRIPT_DIR/requirements.txt"
    /usr/bin/python3 /root/performance-server-script/$SCRIPT_NAME
    nohup python3 -m http.server 8888 --directory /root > /var/log/http_server.log 2>&1 &
else
    echo "No requirements.txt found. Skipping Python dependencies installation."
fi

echo "Adding cron jobs..."
(crontab -l 2>/dev/null | grep -v "$SCRIPT_NAME"; echo "$CRON_JOB") | crontab -

echo "Setup complete. The script will run every hour, and the HTTP server will start on boot."