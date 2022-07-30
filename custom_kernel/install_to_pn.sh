#!/usr/bin/env sh
target="graphics"

cd linux/pack
scp rk3566-pinenote-v1.2.dtb root@pinenote:/extlinux/${target}/
scp Image root@pinenote:/extlinux/${target}/
rsync --delete -avh --progress lib/modules/5.17.0-rc6-next-20220304-* root@pinenote:/lib/modules/
cd ../..
