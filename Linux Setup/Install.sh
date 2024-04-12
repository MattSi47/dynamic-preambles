#!/bin/bash

# Define the password variable
password="uconn"

# Define an array of IP addresses
ip_addresses=("137.99.252.154" "137.99.252.3" "137.99.252.208")



# Iterate over each IP address
for ip_address in "${ip_addresses[@]}"; do
    echo "Running Install Script for $ip_address..."
    echo "Connecting to remote host with username 'uconn' at $ip_address..."
    sshpass -p "$password" ssh -o StrictHostKeyChecking=no uconn@$ip_address << EOF
            echo "Connected to remote host"

            echo "$password" | sudo -S echo && sudo -s apt-get -y update
            echo "$password" | sudo -S echo && sudo -s apt-get -y install git vim cmake build-essential
            echo "$password" | sudo -S echo && sudo -s apt-get -y install uhd-host
            echo "$password" | sudo -S echo && sudo -s cp /usr/lib/uhd/utils/uhd-usrp.rules /etc/udev/rules.d/
            echo "$password" | sudo -S echo && sudo -s udevadm control --reload-rules
            echo "$password" | sudo -S echo && sudo -s udevadm trigger
            echo "$password" | sudo -S echo && sudo -s uhd_images_downloader
            echo "$password" | sudo -S echo && sudo -s apt-get -y install gnuradio-dev python3-packaging
        
            cd /home/uconn
            mkdir sdr

            cd sdr
            echo "$password" | sudo -S echo && sudo -s  apt-get -y install libsndfile1-dev
            git clone https://github.com/bastibl/gr-foo
            cd gr-foo
            mkdir build
            cd build
            cmake ..
            make
            echo "$password" | sudo -S echo && sudo -s make install       
            echo "$password" | sudo -S echo && sudo -s ldconfig

            cd /home/uconn/sdr
            git clone https://github.com/bastibl/gr-ieee802-11
            cd gr-ieee802-11
            mkdir build
            cd build
            cmake ..
            make
            echo "$password" | sudo -S echo && sudo -s make install
            echo "$password" | sudo -S echo && sudo -s ldconfig
            echo "$password" | sudo -S echo && sudo -s sysctl -w kernel.shmmax=2147483648

            cd /home/uconn/sdr
            git clone https://github.com/bastibl/gr-ieee802-15-4
            cd gr-ieee802-15-4
            mkdir build
            cd build
            cmake ..
            make
            echo "$password" | sudo -S echo && sudo -s make install
            echo "$password" | sudo -S echo && sudo -s ldconfig

            cd /home/uconn/sdr
            git clone https://github.com/cloud9477/gr-advoqpsk.git
            cd gr-advoqpsk
            mkdir build
            cd build
            cmake ..
            make
            echo "$password" | sudo -S echo && sudo -s make install
            echo "$password" | sudo -S echo && sudo -s ldconfig

            cd /home/uconn/
            git clone https://github.com/MattSi47/dynamic-preambles.git
            cd /home/uconn/dynamic-preambles/GNURADIO/Modules/gr-UConn2402
            mkdir build
            cd build
            cmake ..
            make
            echo "$password" | sudo -S echo && sudo -s make install
            echo "$password" | sudo -S echo && sudo -s ldconfig

            echo "$password" | sudo -S echo && sudo snap install code --classic

EOF
    echo "Done for $ip_address..."
done
