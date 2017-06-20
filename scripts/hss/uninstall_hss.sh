#!/bin/bash

sudo apt-get -y remove mysql-server libmysqlclient-dev

sudo apt-get -y autoremove

# make clean