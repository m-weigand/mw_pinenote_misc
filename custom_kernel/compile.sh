#!/usr/bin/env sh
cd linux
make clean
make ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- pinenote_defconfig
make -j 2 ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- all
test -d pack && rm -r pack
mkdir pack
make ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- INSTALL_MOD_PATH=${PWD}/pack modules_install
make ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- INSTALL_PATH=${PWD}/pack dtbs_install
cp ./arch/arm64/boot/dts/rockchip/rk3566-pinenote-v1.2.dtb pack/
cp ./arch/arm64/boot/Image pack/

# just modifying the device tree
# vim arch/arm64/configs/pinenote_defconfig
# vim ./arch/arm64/boot/dts/rockchip/rk3566-pinenote-v1.2.dts
# vim ./arch/arm64/boot/dts/rockchip/rk3566-pinenote.dtsi
# make -j 2 ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- dtbs
