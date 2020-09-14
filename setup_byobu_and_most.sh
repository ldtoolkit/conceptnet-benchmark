#!/usr/bin/env sh

sudo apt update
sudo apt install --assume-yes byobu mosh
sudo ufw allow 60000:61000/udp

