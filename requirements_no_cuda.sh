#!/bin/bash
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

git clone https://github.com/json87/SphereSfM.git
cd SphereSfM

sudo apt install -y cmake
cmake --version

mkdir build
cd build

cmake .. -GNinja

ninja

sudo ninja install

export DISPLAY=":99.0"
export QT_QPA_PLATFORM="offscreen"

Xvfb :99 &
