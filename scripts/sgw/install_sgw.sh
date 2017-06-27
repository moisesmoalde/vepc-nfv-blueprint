#!/bin/bash -e

TEMP_DIR="/tmp"
SGW_DIR_NAME="vepc-nfv-blueprint-master"
SGW_DIR=${TEMP_DIR}/${SGW_DIR_NAME}
mkdir -p ${SGW_DIR}

ctx logger debug "${COMMAND}"

ctx logger info "Configure the APT software"
sudo apt-get -y update

set +e
ctx logger info "Installing g++ compiler and make tool"
sudo DEBIAN_FRONTEND=noninteractive apt-get install g++ build-essential --yes --force-yes
ctx logger info "Installing unzip package"
sudo DEBIAN_FRONTEND=noninteractive apt-get install unzip --yes --force-yes
set -e

ctx logger info "Downloading vEPC blueprint package"
wget https://github.com/moisesmoalde/vepc-nfv-blueprint/archive/master.zip -O ${SGW_DIR}.zip
unzip ${SGW_DIR}.zip -d ${TEMP_DIR} && rm ${SGW_DIR}.zip

ctx logger info "Making sgw.out file"
sudo make -C ${SGW_DIR}/src sgw.out

# Runtime property used by start_sgw script
ctx instance runtime-properties sgw_dir ${SGW_DIR}

ctx logger info "SGW successfully installed"
