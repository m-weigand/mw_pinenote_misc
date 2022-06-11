#!/usr/bin/env python
import random
import fcntl
import ctypes


class DrmRockchipEbcInfo1(ctypes.Structure):
    _fields_ = [
        ("info1", ctypes.c_uint64),
        ("info2", ctypes.c_uint64),
    ]


class offscreen(ctypes.Structure):
    _fields_ = [
        ("info1", ctypes.c_int64),
        ("ptr_screen_content", ctypes.POINTER(ctypes.c_char_p)),
        # ("ptr_screen_content", ctypes.c_char_p),
    ]


_IOC_NRBITS     = 8
_IOCtype_BITS   = 8
_IOC_SIZEBITS   = 14
_IOC_DIRBITS    = 2

_IOC_NRMASK     = ((1 << _IOC_NRBITS)-1)
_IOCtype_MASK   = ((1 << _IOCtype_BITS)-1)
_IOC_SIZEMASK   = ((1 << _IOC_SIZEBITS)-1)
_IOC_DIRMASK    = ((1 << _IOC_DIRBITS)-1)

_IOC_NRSHIFT    = 0
_IOCtype_SHIFT  = (_IOC_NRSHIFT+_IOC_NRBITS)
_IOC_SIZESHIFT  = (_IOCtype_SHIFT+_IOCtype_BITS)
_IOC_DIRSHIFT   = (_IOC_SIZESHIFT+_IOC_SIZEBITS)

_IOC_NONE       = 0
_IOC_WRITE      = 1
_IOC_READ       = 2

def _IOC(_dir,type_,nr,size):
    return ((_dir)  << _IOC_DIRSHIFT) | \
           ((type_) << _IOCtype_SHIFT) | \
           ((nr)   << _IOC_NRSHIFT) | \
           ((size) << _IOC_SIZESHIFT)

def _IOCtype_CHECK(t):
    return ctypes.sizeof(t)

def _IO(type_,nr):
    return _IOC(_IOC_NONE,(type_),(nr),0)

def _IOR(type_,nr,size):
    return _IOC(_IOC_READ,(type_),(nr),(_IOCtype_CHECK(size)))

def _IOW(type_,nr,size):
    return _IOC(_IOC_WRITE,(type_),(nr),(_IOCtype_CHECK(size)))

def _IOWR(type_,nr,size):
    return _IOC(_IOC_READ|_IOC_WRITE,(type_),(nr),(_IOCtype_CHECK(size)))

DRM_IOCTL_BASE = ord('d')

def DRM_IOWR(nr, type_):
    return _IOWR(DRM_IOCTL_BASE, nr, type_)

DRM_IOCTL_ROCKCHIP_EBC_INFO_1 = DRM_IOWR(0x40, DrmRockchipEbcInfo1)
DRM_IOCTL_ROCKCHIP_EBC_INFO_2 = DRM_IOWR(0x41, offscreen)

# filename = "/dev/dri/card0"
filename = "/dev/dri/by-path/platform-fdec0000.ebc-card"

fd = open(filename, 'w+b', buffering=0)

arg = DrmRockchipEbcInfo1()
arg.info1 = 1
arg.info2 = 6

# import struct
# arg = struct.pack('QQ', 3000, 7)
r = fcntl.ioctl(fd, DRM_IOCTL_ROCKCHIP_EBC_INFO_1, arg)
print(r)

# ########
# pixel_nr = 1314144
# image = open('feli_bert.bin', 'rb').read()
# assert len(image) == pixel_nr
# screen = ctypes.create_string_buffer(image)
# # screen = ctypes.create_string_buffer(b'\000' * pixel_nr)

# print('generating random screen information')
# # for i in range(0, len(screen)):
# #     screen[i] = random.randint(0, 255)
# # for i in range(0, 10000):
# #     screen[i] = 0
# # for i in range(10000, 100000):
# #     screen[i] = 255
# # for i in range(100000, 1313144):
# #     screen[i] = 0b11001100
# # for i in range(0, len(screen)):
# #     screen[i] = 0

# obj = offscreen()
# obj.info1 = 3001

# screen1 = ctypes.c_char_p()
# screen1.value = 123
# # obj.ptr_screen_content = ctypes.pointer(screen1)
# obj.ptr_screen_content = ctypes.cast(
#     ctypes.pointer(screen),
#     ctypes.POINTER(ctypes.c_char_p),
# )
# print('Sending ioctl now')
# r = fcntl.ioctl(fd, DRM_IOCTL_ROCKCHIP_EBC_INFO_2, obj)
# print(r)
