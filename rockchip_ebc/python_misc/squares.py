import pydrm
import time

# Initialize the screen to white
drm = pydrm.SimpleDrm()
drm.draw.rectangle(((0, 0), (drm.framebuffer.width, drm.framebuffer.height)), fill='white', width=0)
drm.flush()

box_size = 31
box_shift = box_size // 1
box_x = box_size
box_x_mult = -1
box_y = box_size
box_y_mult = -1
max_x = drm.framebuffer.width
max_y = drm.framebuffer.height

while True:
    new_x = box_x + box_shift * box_x_mult
    if new_x < 0 or new_x >= max_x - box_size:
        box_x_mult = -box_x_mult
        new_x = box_x + box_shift * box_x_mult
    new_y = box_y + box_shift * box_y_mult
    if new_y < 0 or new_y >= max_y - box_size:
        box_y_mult = -box_y_mult
        new_y = box_y + box_shift * box_y_mult
    for y in range(new_y, new_y + box_size):
        for x in range(new_x, new_x + box_size):
            offset = (y * drm.framebuffer.width + x) * 4
            # Uncomment this for GRAY16
            px = drm.framebuffer.bo.map[offset] - 0x40
            if (px < 0):
                px += 0x100
            # [end]
            # Uncomment this for GRAY2
            #px = 0xff - drm.framebuffer.bo.map[offset]
            # [end]
            for sub in range(4):
                drm.framebuffer.bo.map[offset + sub] = px
    pydrm.framebuffer.DrmFramebuffer.flush(drm.framebuffer, new_x, new_y, new_x + box_size, new_y + box_size)
    # Uncomment this for one box at a time
    #for y in range(box_y, box_y + box_size):
    #    for x in range(box_x, box_x + box_size):
    #        offset = (y * drm.framebuffer.width + x) * 4
    #        px = 0xff
    #        for sub in range(4):
    #            drm.framebuffer.bo.map[offset + sub] = px
    #pydrm.framebuffer.DrmFramebuffer.flush(drm.framebuffer, box_x, box_y, box_x + box_size, box_y + box_size)
    #time.sleep(1/85)
    # [end]
    box_x = new_x
    box_y = new_y
