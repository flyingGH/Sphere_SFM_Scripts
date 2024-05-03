#!/bin/bash
sudo apt-get update
sudo apt-get install -y \
    cmake \
    libgoogle-glog-dev \
    libgflags-dev \
    libatlas-base-dev \
    libeigen3-dev \
    libsuitesparse-dev

wget http://ceres-solver.org/ceres-solver-2.2.0.tar.gz
tar zxf ceres-solver-2.2.0.tar.gz
mkdir ceres-bin && cd ceres-bin
cmake ../ceres-solver-2.2.0
make -j3
sudo make install
