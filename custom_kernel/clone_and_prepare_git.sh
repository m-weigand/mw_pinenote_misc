#!/usr/bin/env sh

git clone --depth 100 --branch rk35/pinenote-next https://github.com/smaeul/linux.git

# external patches
# Battery-level patch
wget -nc https://github.com/DorianRudolph/linux/commit/822294664906499682b55264ae0553ee05caa352.patch
cd linux
git apply ../822294664906499682b55264ae0553ee05caa352.patch
cd ..

# touchscreen driver
wget -nc https://gitlab.com/pgwipeout/linux-next/-/commit/a24cb29eca1a72afb1037f5468d3036b34ea1b66.patch
wget -nc https://gitlab.com/pgwipeout/linux-next/-/commit/d6bb8a6b5a5210fea70bc590350bfca3a9e3a7a2.patch
cd linux
git apply ../a24cb29eca1a72afb1037f5468d3036b34ea1b66.patch
git apply ../d6bb8a6b5a5210fea70bc590350bfca3a9e3a7a2.patch
cd ..

# My modifications
wget -nc https://raw.githubusercontent.com/m-weigand/mw_pinenote_misc/main/custom_kernel/pinenote_defconfig.patch
wget -nc https://raw.githubusercontent.com/m-weigand/mw_pinenote_misc/main/custom_kernel/rk3566-pinenote_dtsi.patch

# the rockchip_ebc modifications
wget -nc https://raw.githubusercontent.com/m-weigand/mw_pinenote_misc/main/rockchip_ebc/patches/rockchip_ebc_patches_mw_20220622.patch

cd linux
git apply ../pinenote_defconfig.patch
git apply ../rk3566-pinenote_dtsi.patch
git apply ../rockchip_ebc_patches_mw_20220622.patch
cd ..
