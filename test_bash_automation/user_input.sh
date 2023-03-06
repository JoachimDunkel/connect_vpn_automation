#!/bin/bash

# This is just an example of the eventual automation.

# Tail runs indefinetly wich the vpn also does so thats good.

echo "Enter your username: "
read name

echo "Enter password: "
read password

echo "Username: $name, Password: $password."



tail -f /dev/null