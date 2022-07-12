# Misc Pinenote thingies

So I got a Pinenote and started to work on getting Debian to run on this nice little piece of hardware.

This repository contains various documents and patches that I hope prove useful to others also playing
around with their Pinenote.

## Videos

A few videos can be found in (videos)[videos]

## Kernel Patches

I added a few small quality-of-live features to the eink display controller driver developed by smaeul (https://github.com/smaeul/linux/tree/rk35/pinenote-next). Those patches and corresponding documentation can be found here: [ebc patches](rockchip_ebc/patches/).

My kernel configuration and patch level can be reproduced using this script: [custom_kernel/clone_and_prepare_git.sh](custom_kernel/clone_and_prepare_git.sh). This includes my modifications.

## Reading and modifying waveform files using Python

Reading, modifying and writing waveform files is useful to optimize the existing waveforms or generate new ones.

A rudimentary Python interface for reading/writing these waveform files can be found in [waveforms](waveforms).

As a working (and useful) example, the A2 waveform was shortened to 5 phases and white->white and black->black transitions were added.
