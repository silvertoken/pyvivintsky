from homeauto.api_vivint.pyvivintsky.vivint_device import VivintDevice
from homeauto.house import register_sensor_event
import logging
# This retrieves a Python logging instance (or creates it)
logger = logging.getLogger(__name__)


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
        logger.debug(super().get_device()[u"n"] + " is now " + self.state())
        register_sensor_event("Vivint", super().id(), self.state())



