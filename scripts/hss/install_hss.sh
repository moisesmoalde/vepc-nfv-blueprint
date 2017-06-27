#!/bin/bash -e

TEMP_DIR="/tmp"
HSS_DIR_NAME="vepc-nfv-blueprint-master"
HSS_DIR=${TEMP_DIR}/${HSS_DIR_NAME}
mkdir -p ${HSS_DIR}

ctx logger debug "${COMMAND}"

ctx logger info "Configure the APT software"
sudo apt-get -y update

sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password password'
sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password'

set +e
ctx logger info "Installing MySQL packages"
sudo DEBIAN_FRONTEND=noninteractive apt-get install mysql-server libmysqlclient-dev --yes --force-yes
ctx logger info "Installing g++ compiler"
sudo DEBIAN_FRONTEND=noninteractive apt-get install g++ --yes --force-yes
ctx logger info "Installing unzip package"
sudo DEBIAN_FRONTEND=noninteractive apt-get install unzip --yes --force-yes
set -e

ctx logger info "Downloading vEPC blueprint package"
wget https://github.com/moisesmoalde/vepc-nfv-blueprint/archive/master.zip -O ${HSS_DIR_NAME}.zip
unzip ${HSS_DIR_NAME}.zip -d ${HSS_DIR} && rm ${HSS_DIR_NAME}.zip

ctx logger info "Inserting authentication data into HSS database"
sudo mysql -u root < ${HSS_DIR}/scripts/hss/hss.sql

ctx logger info "Making hss.out file"
cd ${HSS_DIR}/src && make hss.out

# Runtime property used by start_hss script
ctx instance runtime-properties hss_dir ${HSS_DIR}

ctx logger info "HSS successfully installed"
