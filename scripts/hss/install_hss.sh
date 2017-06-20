#!/bin/bash -e

sudo apt-get -y update

sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password password'
sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password'

sudo apt-get -y install mysql-server libmysqlclient-dev

#sudo mysql -u root < hss.sql

# make hss.out