#!/bin/bash

if [ -n "$(cat /etc/os-release 2>/dev/null | grep "archarm")" ]; then
    rm -rf mutter

    asp export mutter || (echo "Please install asp: 'pacman -S asp'" && exit 1)

    cd mutter

    patch -p1 < "../asp_mutter_PKGBUILD.patch"
    makepkg -si

    cd ..
else
    # apt build-dep mutter
    # apt source mutter
    test -e mutter.patch || wget -o mutter.patch https://gitlab.com/hrdl/pinenote-shared/-/raw/main/patches/mutter/0001-Add-META_CONNECTOR_TYPE_DPI.patch?inline=false
    rm *.deb
    cd mutter-42.3
    time DEB_BUILD_OPTIONS=nocheck dpkg-buildpackage --build=binary
    cd ..
    # dpkg -i libmutter-9-0_41.4-1_arm64.deb
fi
