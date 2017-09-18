#!/bin/bash -e

TEMP_DIR="/tmp"
PGW_DIR_NAME="vepc-nfv-blueprint-master"
PGW_DIR=${TEMP_DIR}/${PGW_DIR_NAME}
mkdir -p ${PGW_DIR}

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
wget https://github.com/moisesmoalde/vepc-nfv-blueprint/archive/master.zip -O ${PGW_DIR}.zip
unzip ${PGW_DIR}.zip -d ${TEMP_DIR} && rm ${PGW_DIR}.zip

ctx logger info "Making pgw.out file"
sudo make -C ${PGW_DIR}/src pgw.out

ctx logger info "Installing KVStore client"
sudo make -C ${PGW_DIR}/KeyValueStore/Implementation/LevelDB/client/src

# Runtime property used by start_hss script
ctx instance runtime-properties pgw_dir ${PGW_DIR}

ctx logger info "PGW successfully installed"
