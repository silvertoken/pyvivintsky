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

    @property
    def state(self):
        """Returns the state of the device."""
        return self.GarageDoorState(self.get_device().get("s"))

    def update_device(self, updates):
        super().update_device(updates)
        logger.debug(f"{self.name} is now {self.state.name}")

    async def close_garage_door(self):
        """Closes a garage dooor."""
        panel = self.get_root()
        await panel.get_api().set_garage_door_state(
            panel.id,
            self.id,
            self.GarageDoorState.Closing.value,
        )

    async def open_garage_door(self):
        """Opens a garage dooor."""
        panel = self.get_root()
        await panel.get_api().set_garage_door_state(
            panel.id,
            self.id,
            self.GarageDoorState.Opening.value,
        )
