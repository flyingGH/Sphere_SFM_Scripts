#!/bin/bash
ubuntuVersion='22.04'
cudaEnabled=true
asanEnabled=false

# Libraries Regarding Sphere-sfm
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
  xvfb

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

#clone the SphereSfm Repo
git clone https://github.com/json87/SphereSfM.git
cd SphereSfM

#install cuda-gcc - assuming Cuda setup is already done
sudo apt-get install -y \
  nvidia-cuda-toolkit-gcc \
  gcc-10 g++-10

# These are most important
export CC=/usr/bin/gcc-10
export CXX=/usr/bin/g++-10
export CUDAHOSTCXX=/usr/bin/g++-10

# install cmake if not there
# sudo apt install -y cmake
cmake --version
mkdir build && cd build
cmake .. \
  -GNinja \
  -DCMAKE_CUDA_ARCHITECTURES=50 
ninja

# Setup display before executing 
export DISPLAY=":99.0"
export QT_QPA_PLATFORM="offscreen"
Xvfb :99 &
