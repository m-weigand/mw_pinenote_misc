#!/usr/bin/env python
import random
import fnctl
import ctypes
# struct drm_rockchip_ebc_info_2 {
#     __u64 info1;
#     __u64 ptr_screen_content;
# };


class offscreen(ctypes.Structure):
    _fields_ = [
        ("info1", ctypes.c_int64),
        ("ptr_screen_content", ctypes.POINTER(ctypes.c_char)),
    ]


pixel_nr = 1314144
screen = ctypes.create_string_buffer(b'\000' * pixel_nr)
for i in range(0, len(screen)):
    screen[i] = random.randint(0, 255)


obj = offscreen()
obj.info1 = 3001
obj.ptr_screen_content = ctypes.cast(
    ctypes.pointer(screen),
    ctypes.POINTER(ctypes.c_char),

)
