#!/bin/bash -e

TEMP_DIR="/tmp"
HSS_DIR_NAME="vepc-nfv-blueprint-master"
HSS_DIR=${TEMP_DIR}/${HSS_DIR_NAME}
mkdir -p ${HSS_DIR}

ctx logger debug "${COMMAND}"

ctx logger info "Configure the APT software"
sudo apt-get -y update

sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password password mysql'
sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password mysql'

set +e
ctx logger info "Installing MySQL packages"
sudo DEBIAN_FRONTEND=noninteractive apt-get install mysql-server libmysqlclient-dev --yes --force-yes
ctx logger info "Installing g++ compiler and make tool and libboost"
sudo DEBIAN_FRONTEND=noninteractive apt-get install g++ build-essential libboost-all-dev --yes --force-yes
ctx logger info "Installing unzip package"
sudo DEBIAN_FRONTEND=noninteractive apt-get install unzip --yes --force-yes
set -e

ctx logger info "Downloading vEPC blueprint package"

sudo wget https://github.com/moisesmoalde/vepc-nfv-blueprint/archive/master.zip -O ${HSS_DIR}.zip
sudo unzip ${HSS_DIR}.zip -d ${TEMP_DIR} && sudo rm ${HSS_DIR}.zip

ctx logger info "Inserting authentication data into HSS database"
sudo mysql -u root -pmysql < ${HSS_DIR}/scripts/hss/hss.sql

ctx logger info "Making hss.out file"
sudo make -C ${HSS_DIR}/src hss.out

# Runtime property used by start_hss script
ctx instance runtime-properties hss_dir ${HSS_DIR}

ctx logger info "HSS successfully installed"
