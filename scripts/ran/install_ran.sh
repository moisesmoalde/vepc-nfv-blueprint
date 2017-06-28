#!/bin/bash -e

RAN_DIR_NAME="vepc-nfv-blueprint-master"
RAN_DIR=/home/$(whoami)/${RAN_DIR_NAME}
mkdir -p ${RAN_DIR}

ctx logger debug "${COMMAND}"

ctx logger info "Configure the APT software"
sudo apt-get -y update

set +e
ctx logger info "Installing SSL packages"
sudo DEBIAN_FRONTEND=noninteractive apt-get install openssl libssl-dev openvpn --yes --force-yes

ctx logger info "Installing traffic generation packages"
sudo DEBIAN_FRONTEND=noninteractive apt-get install software-properties-common --yes --force-yes
sudo add-apt-repository -y "ppa:patrickdk/general-lucid"
sudo apt-get -y update
sudo DEBIAN_FRONTEND=noninteractive apt-get install iperf3 iperf htop --yes --force-yes

ctx logger info "Installing g++ compiler and make tool"
sudo DEBIAN_FRONTEND=noninteractive apt-get install g++ build-essential --yes --force-yes
ctx logger info "Installing unzip package"
sudo DEBIAN_FRONTEND=noninteractive apt-get install unzip --yes --force-yes
set -e

ctx logger info "Downloading vEPC blueprint package"
wget https://github.com/moisesmoalde/vepc-nfv-blueprint/archive/master.zip -O ${RAN_DIR}.zip
unzip ${RAN_DIR}.zip -d ~ && rm ${RAN_DIR}.zip

# Runtime property used by uninstall_ran script
ctx instance runtime-properties ran_dir ${RAN_DIR}

ctx logger info "RAN successfully installed"
