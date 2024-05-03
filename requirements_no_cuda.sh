#!/bin/bash
# Libraries needed for sphere-sfm Setup
sudo apt-get update && sudo apt-get install -y \
  build-essential \
  ninja-build \
  libboost-program-options-dev \
  libboost-filesystem-dev \
  libboost-graph-dev \
  libboost-system-dev \
  libboost-test-dev \
  libeigen3-dev \
  libceres-dev \
  libflann-dev \
  libfreeimage-dev \
  libmetis-dev \
  libgoogle-glog-dev \
  libgflags-dev \
  libsqlite3-dev \
  libglew-dev \
  qtbase5-dev \
  libqt5opengl5-dev \
  libcgal-dev \
  libcgal-qt5-dev \
  libgl1-mesa-dri \
  libunwind-dev \
  awscli \
  xvfb

#Ceres must be installed before

# ceres installation skip if installed
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

#Clone Repo
git clone https://github.com/json87/SphereSfM.git
cd SphereSfM

# Install cmake
sudo apt install -y cmake
cmake --version

mkdir build && cd build

#Start build
cmake .. -GNinja
ninja

#install the build
sudo ninja install

# Export to see colmap display
export DISPLAY=":99.0"
export QT_QPA_PLATFORM="offscreen"

Xvfb :99 &
