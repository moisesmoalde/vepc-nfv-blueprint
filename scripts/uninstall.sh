#!/bin/bash

sudo apt-get -y remove iperf3 iperf htop

sudo add-apt-repository -r -y "ppa:patrickdk/general-lucid"

sudo apt-get -y remove mysql-server libmysqlclient-dev openvpn libsctp-dev openssl libssl-dev
