#!/usr/bin/env python
# based on https://distfiles.smaeul.xyz/distfiles/tmp/squares.py

# Draw overlapping cubes to test the area splitting functionality
import subprocess

import pydrm
import time

minor = int(
    subprocess.check_output(
        'ls -l /dev/dri/by-path/ | grep ebc | rev | cut -c 1',
        shell=True
    )
)
print('Todays minor number', minor)

# Initialize the screen to white
drm = pydrm.SimpleDrm(minor=minor)
time.sleep(2)

while(True):
    drm.draw.rectangle(
        (
            (0, 0),
            (drm.framebuffer.width, drm.framebuffer.height)
        ), fill='white', width=0
    )
    drm.flush()

    print('sleeping 5 seconds')
    time.sleep(5)
    print('done')
    # print('Press ENTER to continue')
    # input()


    def draw_rect(x1, x2, y1, y2, color=0):
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                offset = (y * drm.framebuffer.width + x) * 4
                # black = 0x00
                # drm.framebuffer.bo.map[offset] = 0x00
                for sub in range(4):
                    drm.framebuffer.bo.map[offset + sub] = color
        return [x1, y1, x2 + 1, y2 + 1]


    flush_list = []
    for i in range(0, 1100, 68):
    # for i in range(0, 200, 100):
        print('Drawing rect')
        ret = draw_rect(i, i + 79, i, i + 79)
        flush_list += [ret]
        # delay a bit so drawing starts on the previous rect
        # time.sleep(0.07)

    for i in range(0, 1100, 68):
    # for i in range(0, 200, 100):
        print('Drawing rect')
        ret = draw_rect(40 + i, 40 + i + 79, i, i + 79)
        flush_list += [ret]

    for i in reversed(range(0, 1100, 68)):
    # for i in range(0, 200, 100):
        print('Drawing rect')
        ret = draw_rect(40 + i, 40 + i + 79, i, i + 79, color=255)
        flush_list += [ret]

#     for i in range(0, 1100, 68):
#     # for i in range(0, 200, 100):
#         print('Drawing rect')
#         ret = draw_rect(40 + i, 40 + i + 79, i, i + 79, color=125)
#         flush_list += [ret]

#     for i in range(0, 1100, 68):
#     # for i in range(0, 200, 100):
#         print('Drawing rect')
#         ret = draw_rect(60 + i, 60 + i + 79, i, i + 79, color=255)
#         flush_list += [ret]

    # now flush the regions
    for clip in flush_list:
        pydrm.framebuffer.DrmFramebuffer.flush(
            drm.framebuffer,
            *clip
        )
        time.sleep(0.05)

    print('Press ENTER to finish')
    input()
