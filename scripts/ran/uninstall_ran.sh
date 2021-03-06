#!/bin/bash -e

RAN_DIR=$(ctx instance runtime-properties ran_dir)
sudo rm -r ${RAN_DIR}

sudo apt-get -y remove iperf3 iperf htop openssl libssl-dev openvpn
sudo add-apt-repository -y -r "ppa:patrickdk/general-lucid"
sudo apt-get -y autoremove
