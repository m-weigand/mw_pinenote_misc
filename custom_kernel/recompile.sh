#!/usr/bin/env sh

cd linux
make -j 2 ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- all
if [ $? -ne 0 ];then
	exit 1
fi
test -d pack && rm -r pack
mkdir pack
make ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- INSTALL_MOD_PATH=${PWD}/pack modules_install
make ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- INSTALL_PATH=${PWD}/pack dtbs_install
cp ./arch/arm64/boot/dts/rockchip/rk3566-pinenote-v1.2.dtb pack/
cp ./arch/arm64/boot/Image pack/
