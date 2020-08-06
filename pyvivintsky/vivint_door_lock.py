from pyvivintsky.vivint_device import VivintDevice


class VivintDoorLock(VivintDevice):
    """
    Generic Door Lock Device.
    """
    DEVICE_STATES = {True: "Locked", False: "Unlocked"}

    def __init__(self, device, root):
        super().__init__(device, root)

    def state(self):
        """Returns Locked or Unlocked based on the state of the device."""
        return self.DEVICE_STATES[super().get_device()[u"s"]]

    def update_device(self, updates):
        super().update_device(updates)
        print(super().get_device()[u"n"] + " is now " + self.state())



