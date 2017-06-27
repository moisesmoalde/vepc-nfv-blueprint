B#!/bin/bash -e

SINK_DIR_NAME="vepc-nfv-blueprint-master"
SINK_DIR=/home/$(whoami)/${SINK_DIR_NAME}
mkdir -p ${SINK_DIR}

ctx logger debug "${COMMAND}"

ctx logger info "Configure the APT software"
sudo apt-get -y update

set +e
ctx logger info "Installing traffic generation packages"
sudo DEBIAN_FRONTEND=noninteractive apt-get install software-properties-common --yes --force-yes
sudo add-apt-repository -y "ppa:patrickdk/general-lucid"
sudo apt-get -y update
sudo DEBIAN_FRONTEND=noninteractive apt-get install iperf3 iperf htop --yes --force-yes

ctx logger info "Installing g++ compiler"
sudo DEBIAN_FRONTEND=noninteractive apt-get install g++ --yes --force-yes
ctx logger info "Installing unzip package"
sudo DEBIAN_FRONTEND=noninteractive apt-get install unzip --yes --force-yes
set -e

ctx logger info "Downloading vEPC blueprint package"
wget https://github.com/moisesmoalde/vepc-nfv-blueprint/archive/master.zip -O ${SINK_DIR_NAME}.zip
unzip ${SINK_DIR_NAME}.zip -d ${SINK_DIR} && rm ${SINK_DIR_NAME}.zip

# Runtime property used by uninstall_sink script
ctx instance runtime-properties sink_dir ${SINK_DIR}

ctx logger info "SINK successfully installed"
