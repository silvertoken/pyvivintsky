import logging
from enum import Enum

from pyvivintsky.vivint_device import VivintDevice

logger = logging.getLogger(__name__)


class VivintGarageDoor(VivintDevice):
    """Represents a Vivint Garage Door"""

    class GarageDoorState(Enum):
        Unknown = 0
        Closed = 1
        Closing = 2
        Stopped = 3
        Opening = 4
        Opened = 5

    def __init__(self, device, root):
        super().__init__(device, root)

    def state(self):
        """Returns the state of the device."""
        return self.GarageDoorState(super().get_device()[u"s"])

    def update_device(self, updates):
        super().update_device(updates)
        logger.debug(super().get_device()[u"n"] + " is now " + self.state().name)
