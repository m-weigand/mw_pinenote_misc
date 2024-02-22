#!/usr/bin/env sh

# extract the vendor data from a full disc image
dd if=first8MB.bin of=vendor.bin skip=7168 obs=512 count=512
