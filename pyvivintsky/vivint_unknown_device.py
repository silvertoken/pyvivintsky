from pyvivintsky.vivint_device import VivintDevice


class VivintUnknownDevice(VivintDevice):
    """Represents an unknown device"""

    def __init__(self, device, root):
        super().__init__(device, root)
