#!/bin/bash -e

TEMP_DIR="/tmp"
MME_DIR_NAME="vepc-nfv-blueprint-master"
MME_DIR=${TEMP_DIR}/${MME_DIR_NAME}
mkdir -p ${MME_DIR}

ctx logger debug "${COMMAND}"

ctx logger info "Configure the APT software"
sudo apt-get -y update

set +e
ctx logger info "Installing SSL packages"
sudo DEBIAN_FRONTEND=noninteractive apt-get install openssl libssl-dev --yes --force-yes
ctx logger info "Installing g++ compiler and make tool and libboost"
sudo DEBIAN_FRONTEND=noninteractive apt-get install g++ build-essential  libboost-all-dev --yes --force-yes
ctx logger info "Installing unzip package"
sudo DEBIAN_FRONTEND=noninteractive apt-get install unzip --yes --force-yes
set -e

ctx logger info "Downloading vEPC blueprint package"
wget https://github.com/moisesmoalde/vepc-nfv-blueprint/archive/master.zip -O ${MME_DIR}.zip
unzip ${MME_DIR}.zip -d ${TEMP_DIR} && rm ${MME_DIR}.zip

ctx logger info "Making mme.out file"
sudo make -C ${MME_DIR}/src mme.out

# Runtime property used by start_mme script
ctx instance runtime-properties mme_dir ${MME_DIR}

ctx logger info "MME successfully installed"
