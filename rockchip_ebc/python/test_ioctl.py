#!/usr/bin/env python
import fcntl
from pydrm.drm_h import DRM_IOCTL_MODE_GETPLANERESOURCES
from pydrm.drm_h import DRM_IOCTL_SET_CLIENT_CAP
from pydrm.drm_h import DRM_CLIENT_CAP_UNIVERSAL_PLANES
# from pydrm.drm_h import  DRM_IOCTL_MODE_GETPLANE
from pydrm.drm_h import DrmSetClientCapC
from pydrm.drm_mode_h import DrmModeGetPlaneResC
# , DrmModeGetPlaneC, DRM_MODE_OBJECT_PLANE


def drm_set_client_cap(fd, capability, value):
    c = DrmSetClientCapC()
    c.capability = capability
    c.value = value
    fcntl.ioctl(fd, DRM_IOCTL_SET_CLIENT_CAP, c)


filename = "/dev/dri/card0"

fd = open(filename, 'w+b', buffering=0)

drm_set_client_cap(fd, DRM_CLIENT_CAP_UNIVERSAL_PLANES, 1)

arg = DrmModeGetPlaneResC()
arg.plane_count = -1
fcntl.ioctl(fd, DRM_IOCTL_MODE_GETPLANERESOURCES, arg)
