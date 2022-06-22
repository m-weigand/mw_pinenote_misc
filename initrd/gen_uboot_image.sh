#!/bin/bash
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
	--install /lib/firmware/rockchip/ebc.wbf \
	--include ${PWD}/offscreen.bin /usr/lib/firmware/rockchip/rockchip_ebc_default_screen.bin \
	dracut-initrd.img ${version}

mkimage -A arm -T ramdisk -C none -n mw1 -d dracut-initrd.img initrd.img
