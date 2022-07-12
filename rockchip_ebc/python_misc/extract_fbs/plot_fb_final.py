#!/usr/bin/env python
# Plot the contents of the final buffer
# import png
import numpy as np
import matplotlib.pylab as plt
from matplotlib import cm


def get_buffer(filename):
    with open(filename, 'rb') as fid:
        data = fid.read()
    return data


fb_final = get_buffer('fb_final.bin')
image = np.ones((1872 * 1404)).astype(int) * 0
index = 0
for nr, pixel in enumerate(fb_final):
    # print(pixel)
    p1 = pixel & 0b00001111
    # print(p1)
    p2 = pixel & 0b11110000
    # p2 = 0
    image[index] = p1
    image[index + 1] = p2 >> 4
    index = index + 2
print(image.min(), image.max())

image = image.reshape((1404, 1872)).astype(int)[::-1, ::-1]
# does not work...
# png.from_array(image, 'L', info={'bitdepth': 4}).save('foo.png')

# restrict to xournalpp drawing area for histogram analysis
# image[0:100, :] = 0
# image[1000:] = 0
# np.histogram(image)

cmap = cm.get_cmap('binary_r', 16)
fig, ax = plt.subplots()
X, Y = np.meshgrid(range(1872), range(1404))
sc = ax.scatter(
    X.flatten(),
    Y.flatten(),
    s=1,
    c=image.flatten(),
    cmap=cmap,
)
ax.set_aspect('equal')
fig.colorbar(sc)
fig.tight_layout()
fig.savefig('plot_fb_final.png', dpi=300)
