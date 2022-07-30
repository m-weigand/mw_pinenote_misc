#!/bin/bash
# generate an initrd image using dracut
# note 1: remove the offscreen.bin include directive if you do not want to
# 		  prepare an off-screen image.
# note 2: the patch set from 2022.July.30 properly announces the required
# firmware file. Older versions must include this parameter
#   --install /lib/firmware/rockchip/ebc.wbf \

# kernel modules
version="5.17.0-rc6-next-20220304-g917a31bb1ac2-dirty"

sync
depmod -a
test -e dracut-initrd.img && rm dracut-initrd.img
test -e initrd.img && rm initrd.img
/usr/bin/dracut -v \
	-o "lvm luks plymouth systemd resume" \
	--add-drivers rockchip_ebc \
	--omit-drivers "bluetooth hidp" \
	--include ${PWD}/offscreen.bin /usr/lib/firmware/rockchip/rockchip_ebc_default_screen.bin \
	dracut-initrd.img ${version}

mkimage -A arm -T ramdisk -C none -n mw1 -d dracut-initrd.img initrd.img
