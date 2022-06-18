# Rockchip_ebc modifications

## Based upon

Smaeuls repository https://github.com/smaeul/linux.git
Branch pinenote-next
commit 0b654237163e30b9812185859e0545b25a75444b

## New features (as of 2022.Jun.18)

* Area splititng (improves xournalpp performance)
* Allow odd start/end coordinates for clips (i.e., 1x1 pixel blits)
* Auto refresh based on partially refreshed screen area
* Adds an ioctl to force a global refresh on next update
* Ability to set the off-screen content via binary file loaded on module-load
  time or via ioctl

* A few changes to the DMA handling of the buffers, which at least for me
  greatly reduces (but not removes) artifacting and ghosting
* A few (subjective?) bug-fixes

## Applications

Check if the patch can be correctly applied:

	cd linux
	git checkout pinenote-next
	patch --dry-run -p1 < rockchip_ebc_patches_mw_20220611.patch

Then remove the **--dry-run** option and rerun to actually apply.
