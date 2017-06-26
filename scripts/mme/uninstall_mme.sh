#!/bin/bash -e

MME_DIR=$(ctx instance runtime-properties mme_dir)
sudo rm -r ${MME_DIR}

sudo apt-get -y remove openssl libssl-dev
sudo apt-get -y autoremove
