# Rockchip_ebc modifications

## Based upon

Smaeuls repository https://github.com/smaeul/linux.git
Branch pinenote-next
commit 0b654237163e30b9812185859e0545b25a75444b

## New features (as of 2022.Jun.11)

* Area splititng (improves xournalpp performance)
* Auto refresh based on partially refreshed screen area
* Adds an ioctl to force a global refresh on next update
* Ability to set the off-screen content via binary file loaded on module-load
  time or via ioctl

* A few changes to the DMA handling of the buffers, which at least for me
  greatly reduces (but not removes) artifacting and ghosting
* A few (subjective?) bug-fixes
