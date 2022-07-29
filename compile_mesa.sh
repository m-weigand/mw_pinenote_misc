#!/bin/bash
test -e rockchip_ebc.patch || wget https://raw.githubusercontent.com/0cc4m/pinenote-misc/main/mesa-archlinux-arm/mesa/rockchip_ebc.patch
rm *.deb
cd mesa-22.1.3
patch -N -p1 -i ../rockchip_ebc.patch
time DEB_BUILD_OPTIONS=nocheck dpkg-buildpackage --build=binary
cd ..
# dpkg -i libmutter-9-0_41.4-1_arm64.deb
