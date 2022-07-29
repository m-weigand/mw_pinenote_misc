#!/bin/bash
rm *.deb
cd mutter-42.3
time DEB_BUILD_OPTIONS=nocheck dpkg-buildpackage --build=binary
cd ..
# dpkg -i libmutter-9-0_41.4-1_arm64.deb
