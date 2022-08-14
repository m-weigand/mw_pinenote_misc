#!/bin/bash

test -e rockchip_ebc.patch || wget https://raw.githubusercontent.com/0cc4m/pinenote-misc/main/mesa-archlinux-arm/mesa/rockchip_ebc.patch

if [ -n "$(cat /etc/os-release 2>/dev/null | grep "archarm")" ]; then
    rm -rf mesa

    asp export mesa || (echo "Please install asp: 'pacman -S asp'" && exit 1)

    cd mesa

    patch -p1 < "../asp_mesa_PKGBUILD.patch"
    gpg --recv-keys 4C95FAAB3EB073EC
    makepkg -si

    cd ..
else
    rm *.deb
    cd mesa-22.1.3
    patch -N -p1 -i ../rockchip_ebc.patch
    time DEB_BUILD_OPTIONS=nocheck dpkg-buildpackage --build=binary
    cd ..
    # dpkg -i libmutter-9-0_41.4-1_arm64.deb
fi

