#!/bin/bash -e

HSS_DIR=$(ctx instance runtime-properties hss_dir)
sudo rm -r ${HSS_DIR}

sudo apt-get -y remove mysql-server libmysqlclient-dev
sudo apt-get -y autoremove
