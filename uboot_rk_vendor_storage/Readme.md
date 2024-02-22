# Python script to extract and modify the vendor data of the rockchip u-boot

## Writing the new vendor block to disc:

	dd if=vendor_fixed.bin of=test.bin seek=7168
