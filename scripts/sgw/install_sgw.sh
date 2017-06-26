#!/bin/bash -e

TEMP_DIR="/tmp"
SGW_DIR_NAME="vepc-nfv-blueprint-master"
SGW_DIR=${TEMP_DIR}/${SGW_DIR_NAME}
mkdir -p ${SGW_DIR}

ctx logger debug "${COMMAND}"

ctx logger info "Configure the APT software"
sudo apt-get -y update

set +e
ctx logger info "Installing g++ compiler"
sudo DEBIAN_FRONTEND=noninteractive apt-get install g++ --yes --force-yes
set -e

ctx logger info "Downloading vEPC blueprint package"
wget https://github.com/moisesmoalde/vepc-nfv-blueprint/archive/master.zip -O ${SGW_DIR_NAME}.zip
unzip ${SGW_DIR_NAME}.zip -d ${SGW_DIR} && rm ${SGW_DIR_NAME}.zip

ctx logger info "Making sgw.out file"
cd ${SGW_DIR}/src && make sgw.out

# Runtime property used by start_sgw script
ctx instance runtime-properties sgw_dir ${SGW_DIR}

ctx logger info "SGW successfully installed"
