#!/bin/bash -e

TEMP_DIR="/tmp"
PGW_DIR_NAME="vepc-nfv-blueprint-master"
PGW_DIR=${TEMP_DIR}/${PGW_DIR_NAME}
mkdir -p ${PGW_DIR}

ctx logger debug "${COMMAND}"

ctx logger info "Configure the APT software"
sudo apt-get -y update

set +e
ctx logger info "Installing g++ compiler"
sudo DEBIAN_FRONTEND=noninteractive apt-get install g++ --yes --force-yes
ctx logger info "Installing unzip package"
sudo DEBIAN_FRONTEND=noninteractive apt-get install unzip --yes --force-yes
set -e

ctx logger info "Downloading vEPC blueprint package"
wget https://github.com/moisesmoalde/vepc-nfv-blueprint/archive/master.zip -O ${PGW_DIR_NAME}.zip
unzip ${PGW_DIR_NAME}.zip -d ${PGW_DIR} && rm ${PGW_DIR_NAME}.zip

ctx logger info "Making pgw.out file"
cd ${PGW_DIR}/src && make pgw.out

# Runtime property used by start_hss script
ctx instance runtime-properties pgw_dir ${PGW_DIR}

ctx logger info "PGW successfully installed"
