# Rockchip_ebc modifications

**WARNING: Due to time constraints these modifications are not well tested! Use with care.**
See the **Usage** section below for information on how to use the new features.

## Based upon

* Smaeuls repository https://github.com/smaeul/linux.git
* Branch pinenote-next
* commit 0b654237163e30b9812185859e0545b25a75444b

## Compiling

Use (this)[../../custom_kernel/clone_and_prepare_git.sh] script to clone the
kernel repo and apply some patches.

Use (this)[../../custom_kernel/compile.sh] script to compile the kernel.

Use (this)[../../initrd/gen_uboot_image.sh] script to generate an initrd image
using dracut.

## New features (as of 2022.July.12)

* Black and white mode
* Area splititng (improves xournalpp performance)
* Allow odd start/end coordinates for clips (i.e., 1x1 pixel blits)
* Auto refresh based on partially refreshed screen area
* Adds an ioctl to force a global refresh on next update
* Ability to set the off-screen content via binary file loaded on module-load
  time or via ioctl

* A few changes to the DMA handling of the buffers, which at least for me
  greatly reduces (but not removes) artifacting and ghosting
* A few (subjective?) bug-fixes

## Applying the patches

Check if the patch can be correctly applied:

	cd linux
	git checkout pinenote-next
	patch --dry-run -p1 < rockchip_ebc_patches_mw_20220623.patch

Then remove the **--dry-run** option and rerun to actually apply.

## Usage

All module parameters are controlled using the sysfs parameters in
/sys/module/rockchip_ebc/parameters

The module parameters can also be set on module load time, for example using
the modprobe configuration file:

	root@pinenote:~# cat /etc/modprobe.d/rockchip_ebc.conf
	options rockchip_ebc direct_mode=0 auto_refresh=1 split_area_limit=0 panel_reflection=1

By default they need to be writen to as root, but this can be easily changed
via udev rules.

### Black and White mode

Activate with

	echo 1 > /sys/module/rockchip_ebc/parameters/bw_mode

the threshold value can be set using:

	echo 7 > /sys/module/rockchip_ebc/parameters/bw_threshold

7 is the default value, meaning that all pixel values lower than 7 will be cast
to 0 (black) and all values larger than, or equal to, 7 will be cast to 15
(white).

### Auto Refresh

Enabling automatic global (full screen) refreshes:

echo 1 > /sys/module/rockchip_ebc/parameters/auto_refresh

Global refreshes are triggered based on the area drawing using partial
refreshes, in units of total screen area.

echo 2 > /sys/module/rockchip_ebc/parameters/refresh_threshold

therefore will trigger a globlal refresh whenever 2 screen areas where drawn.

The threshold should be set according to the application used. For example,
evince and xournalpp really like to redraw the screen very often, so a value of
20 suffices.
Other require lower numbers.

### Off-screen

TODO: Documentation

For now see (../feature_off_screen)[../feature_off_screen] for more
information.

## Open issues

* reflection=0 shows a mirrored screen (as far as I understand this is by
  design and reflects the actual hardware orientation)
* Fix locking: Use the queue_lock to make sure that the final buffer is not
  being written to while contents are blitted to the next buffer.
* Re-evaluate the locking approach: As implemented now the refresh takes a
  little bit longer as we a) wait for each frame to finish before preparing the
  next one, and b) we more aggressively lock in the atomic_update and
  partial_refresh functions. Maybe we need a switch to compromise on image
  quality/consistency and drawing speed?
* Still no idea how to make sure that the final-buffer and the area queue keep
  in sync when lots of damaged areas are reported that overlap and thus
  overwrite the framebuffer. I think in the end to fully fix this we would need
  multiple final buffers and keep track of overlapping areas.
* The off-screen buffers should probably be allocated dynamically based on the
  reported framebuffer size. This would also entail a two-step ioctl approach
  where the first call fills in the fb size and the second one reads a
  pre-allocated user-space memory area.
* The full-refresh ioctl is temporary as this is not a valid use of ioctls. Not
  sure how to modify this so it could potentially be kept. Also, a way for
  non-root users to trigger a full refresh would be nice (we will always
  encounter applications/compositors that will not be aware of the epd
  requirements).
* I'm still seeing gray areas in xournalpp from time to time. This points to a
  bug in the scheduling/area-splitting code. Needs more investigation
