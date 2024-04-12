#!/bin/bash

# Define the password variable
password="uconn"

# Define an array of IP addresses
ip_addresses=("137.99.0.17" "137.99.252.3" "137.99.252.208")



# Iterate over each IP address
for ip_address in "${ip_addresses[@]}"; do
    echo "Running Install Script for $ip_address..."
    echo "Connecting to remote host with username 'uconn' at $ip_address..."
    sshpass -p "$password" ssh -o StrictHostKeyChecking=no uconn@$ip_address << EOF
            echo "Connected to remote host"

            echo "$password" | sudo -S echo && sudo -s apt-get -y update
            cd /home/uconn/dynamic-preambles
            git reset --hard origin/main
            git pull origin main

            cd /home/uconn/dynamic-preambles/GNURADIO/Modules/gr-UConn2402
            gr_modtool bind fftXCorr
            
            cd /home/uconn/dynamic-preambles/GNURADIO/Modules/gr-UConn2402
            echo "$password" | sudo -S echo && sudo -s sh update.sh

            cd /home/uconn/
            echo "$password" | sudo -S echo && sudo rm -r /home/uconn/.grc_gnuradio
            mkdir .grc_gnuradio
            cp -r /home/uconn/dynamic-preambles/GNURADIO//Heir\ Blocks/* /home/uconn/.grc_gnuradio/ 
            
EOF
    echo "Done for $ip_address..."
done
