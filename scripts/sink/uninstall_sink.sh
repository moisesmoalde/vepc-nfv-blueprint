#!/bin/bash -e

SINK_DIR=$(ctx instance runtime-properties sink_dir)
sudo rm -r ${SINK_DIR}

sudo apt-get -y remove iperf3 iperf htop openvpn
sudo add-apt-repository -y -r "ppa:patrickdk/general-lucid"
sudo apt-get -y autoremove
