#!/bin/bash -e

PGW_DIR=$(ctx instance runtime-properties pgw_dir)
sudo rm -r ${PGW_DIR}
