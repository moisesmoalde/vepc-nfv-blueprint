#!/bin/bash -e

ctx logger debug "${COMMAND}"

ctx logger info "Creating main directories and environment variables"
TEMP_DIR="/tmp"
KVSTORE_DIR_NAME="vepc-nfv-blueprint-master"
KVSTORE_DIR=${TEMP_DIR}/${KVSTORE_DIR_NAME}
GO_DIR=${KVSTORE_DIR}/GO

export GOROOT=${GO_DIR}/go
export PATH=$PATH:$GOROOT/bin
export GOPATH=${GO_DIR}/go_workspace

mkdir -p ${KVSTORE_DIR}
mkdir -p ${GO_DIR}
mkdir -p $GOPATH/src/levelmemdb
mkdir -p $GOPATH/pkg/levelmemdb
mkdir -p $GOPATH/bin/levelmemdb

ctx logger info "Configure the APT software"
sudo apt-get update

set +e
ctx logger info "Installing g++ compiler and make tool and git"
sudo apt-get -y install g++ build-essential git
ctx logger info "Installing unzip package"
sudo apt-get -y install unzip
set -e

ctx logger info "Downloading vEPC blueprint package"
wget https://github.com/moisesmoalde/vepc-nfv-blueprint/archive/master.zip -O ${KVSTORE_DIR}.zip
unzip ${KVSTORE_DIR}.zip -d ${TEMP_DIR} && rm ${KVSTORE_DIR}.zip

ctx logger info "Downloading GO server"
wget -nc "https://storage.googleapis.com/golang/go1.6.2.linux-amd64.tar.gz"
tar -C ${GO_DIR} -xzf go1.6.2.linux-amd64.tar.gz

ctx logger info "Installing KVStore"
cp -rp ${KVSTORE_DIR}/KeyValueStore/Implementation/LevelDB/server/src/* $GOPATH/src/levelmemdb
go get -d github.com/syndtr/goleveldb/leveldb
go get -d github.com/syndtr/goleveldb/leveldb/memdb

ctx logger info "KVStore successfully installed"
