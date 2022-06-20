#!/usr/bin/env python
# Retrieve the buffer contents from the prev, next, final buffers of the
# rockchip_ebc driver

# Based upon https://github.com/notro/pydrm :
# https://github.com/notro/pydrm/blob/master/pydrm/drm_h.py
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
    ]


class extract_fbs(ctypes.Structure):
    _fields_ = [
        ("ptr_prev", ctypes.POINTER(ctypes.c_char_p)),
        ("ptr_next", ctypes.POINTER(ctypes.c_char_p)),
        ("ptr_final", ctypes.POINTER(ctypes.c_char_p)),
    ]


_IOC_NRBITS = 8
_IOCtype_BITS = 8
_IOC_SIZEBITS = 14
_IOC_DIRBITS = 2

_IOC_NRMASK = ((1 << _IOC_NRBITS)-1)
_IOCtype_MASK = ((1 << _IOCtype_BITS)-1)
_IOC_SIZEMASK = ((1 << _IOC_SIZEBITS)-1)
_IOC_DIRMASK = ((1 << _IOC_DIRBITS)-1)

_IOC_NRSHIFT = 0
_IOCtype_SHIFT = (_IOC_NRSHIFT+_IOC_NRBITS)
_IOC_SIZESHIFT = (_IOCtype_SHIFT+_IOCtype_BITS)
_IOC_DIRSHIFT = (_IOC_SIZESHIFT+_IOC_SIZEBITS)

_IOC_NONE = 0
_IOC_WRITE = 1
_IOC_READ = 2


def _IOC(_dir, type_, nr, size):
    return ((_dir) << _IOC_DIRSHIFT) | \
           ((type_) << _IOCtype_SHIFT) | \
           ((nr) << _IOC_NRSHIFT) | \
           ((size) << _IOC_SIZESHIFT)


def _IOCtype_CHECK(t):
    return ctypes.sizeof(t)


def _IO(type_, nr):
    return _IOC(_IOC_NONE, (type_), (nr), 0)


def _IOR(type_, nr, size):
    return _IOC(_IOC_READ, (type_), (nr), (_IOCtype_CHECK(size)))


def _IOW(type_, nr, size):
    return _IOC(_IOC_WRITE, (type_), (nr), (_IOCtype_CHECK(size)))


def _IOWR(type_, nr, size):
    return _IOC(_IOC_READ | _IOC_WRITE, (type_), (nr), (_IOCtype_CHECK(size)))


DRM_IOCTL_BASE = ord('d')


def DRM_IOWR(nr, type_):
    return _IOWR(DRM_IOCTL_BASE, nr, type_)


DRM_IOCTL_ROCKCHIP_EBC_INFO_1 = DRM_IOWR(0x40, DrmRockchipEbcInfo1)
DRM_IOCTL_ROCKCHIP_EBC_INFO_2 = DRM_IOWR(0x41, offscreen)
DRM_IOCTL_ROCKCHIP_EBC_EXTRACT_FBS = DRM_IOWR(0x042, extract_fbs)

# filename = "/dev/dri/card0"
filename = "/dev/dri/by-path/platform-fdec0000.ebc-card"

fd = open(filename, 'w+b', buffering=0)

pixel_nr = 1314144
arg = extract_fbs()
bf_prev = ctypes.create_string_buffer(pixel_nr)
bf_next = ctypes.create_string_buffer(pixel_nr)
bf_final = ctypes.create_string_buffer(pixel_nr)

arg.ptr_prev = ctypes.cast(
    ctypes.pointer(bf_prev),
    ctypes.POINTER(ctypes.c_char_p),
)

arg.ptr_next = ctypes.cast(
    ctypes.pointer(bf_next),
    ctypes.POINTER(ctypes.c_char_p),
)

arg.ptr_final = ctypes.cast(
    ctypes.pointer(bf_final),
    ctypes.POINTER(ctypes.c_char_p),
)

r = fcntl.ioctl(fd, DRM_IOCTL_ROCKCHIP_EBC_EXTRACT_FBS, arg)
print(r)
with open('fb_final.bin', 'wb') as fid:
    fid.write(bf_final)
with open('fb_prev.bin', 'wb') as fid:
    fid.write(bf_prev)
with open('fb_next.bin', 'wb') as fid:
    fid.write(bf_next)
