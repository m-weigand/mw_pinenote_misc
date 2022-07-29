#!/bin/bash
# apt build-dep mutter
# apt source mutter
test -e mutter.patch || wget -o mutter.patch https://gitlab.com/hrdl/pinenote-shared/-/raw/main/patches/mutter/0001-Add-META_CONNECTOR_TYPE_DPI.patch?inline=false
rm *.deb
cd mutter-42.3
time DEB_BUILD_OPTIONS=nocheck dpkg-buildpackage --build=binary
cd ..
# dpkg -i libmutter-9-0_41.4-1_arm64.deb
