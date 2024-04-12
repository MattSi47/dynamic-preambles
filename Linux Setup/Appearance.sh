#!/bin/bash

# Define the password variable
password="uconn"

# Define an array of IP addresses
ip_addresses=("137.99.252.154" "137.99.252.3" "137.99.252.208")

# Iterate over each IP address
for ip_address in "${ip_addresses[@]}"; do
    echo "Running Appearance Script for $ip_address..."
    echo "Connecting to remote host with username 'uconn' at $ip_address..."
    sshpass -p "$password" ssh -o StrictHostKeyChecking=no uconn@$ip_address << EOF
        echo "Connected to remote host"

        echo "Setting dock-fixed..."
        gsettings set org.gnome.shell.extensions.dash-to-dock dock-fixed false

        echo "Setting extend-height..."
        gsettings set org.gnome.shell.extensions.dash-to-dock extend-height false

        echo "Setting dock-position..."
        gsettings set org.gnome.shell.extensions.dash-to-dock dock-position BOTTOM

        echo "Setting gtk-theme..."
        gsettings set org.gnome.desktop.interface gtk-theme Yaru-blue

        echo "Creating wallpaper folder..."
        cd 
        cd ~/Pictures 
        mkdir -p wallpapers

        exit
EOF
    echo "Copying wallpaper..."
    sshpass -p "$password" scp background.jpeg uconn@$ip_address:~/Pictures/wallpapers
    sshpass -p "$password" scp background2.jpg uconn@$ip_address:~/Pictures/wallpapers
    wait
    echo "Done for $ip_address..."
done
