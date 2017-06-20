#!/bin/bash

sudo apt-get -y update && sudo apt-get -y upgrade

sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password password'
sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password'

sudo apt-get -y install mysql-server libmysqlclient-dev openvpn libsctp-dev openssl libssl-dev

sudo add-apt-repository -y "ppa:patrickdk/general-lucid"

sudo apt-get -y update

sudo apt-get -y install iperf3 iperf htop
