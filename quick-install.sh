#!/bin/bash

set -e



echo "Cloning UbuntuAI..."



git clone https://github.com/tanishq-agarkar/ubuntuai.git ~/ubuntuai



cd ~/ubuntuai



chmod +x install.sh



./install.sh



echo

echo "Starting UbuntuAI..."



./scripts/run.sh
