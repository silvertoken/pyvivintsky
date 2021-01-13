import logging

from pyvivintsky.vivint_device import VivintDevice

logger = logging.getLogger(__name__)


class VivintDoorLock(VivintDevice):
    """Represents a Vivint Door Lock"""

    LOCK_STATES = {True: "Locked", False: "Unlocked"}

    def __init__(self, device, root):
        super().__init__(device, root)

    @property
    def state(self):
        """Returns Locked or Unlocked based on the state of the device."""
        return self.LOCK_STATES[super().get_device()[u"s"]]

    def update_device(self, updates):
        super().update_device(updates)
        logger.debug(super().get_device()[u"n"] + " is now " + self.state)

    async def lock(self):
        """Lock the lock."""
        panel = super().get_root()
        await panel.get_api().set_lock_state(panel.id, super().id, True)

    async def unlock(self):
        """Unlock the lock."""
        panel = super().get_root()
        await panel.get_api().set_lock_state(panel.id, super().id, False)
