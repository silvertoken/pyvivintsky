from pyvivintsky.vivint_device import VivintDevice


class VivintUnknownDevice(VivintDevice):
    """Represents an unknown device"""

    def __init__(self, json, root):
        super().__init__(json, root)
