#!/usr/bin/env python
# Set the off-screen content using an ioctl. Note that this transient and will
# not be remembered on next reboot! Use the firmware-approach for this.
import random
import fnctl
import ctypes

class offscreen(ctypes.Structure):
    _fields_ = [
        ("info1", ctypes.c_int64),
        ("ptr_screen_content", ctypes.POINTER(ctypes.c_char)),
    ]


# TODO: Read from file
# (1872 x 1404) / 2
pixel_nr = 1314144
# this buffer should contain the pixel values
screen = ctypes.create_string_buffer(b'\000' * pixel_nr)
for i in range(0, len(screen)):
    screen[i] = random.randint(0, 255)


obj = offscreen()
obj.info1 = 3001
obj.ptr_screen_content = ctypes.cast(
    ctypes.pointer(screen),
    ctypes.POINTER(ctypes.c_char),

)
