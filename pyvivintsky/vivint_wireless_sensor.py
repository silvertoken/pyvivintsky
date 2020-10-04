from homeauto.api_vivint.pyvivintsky.vivint_device import VivintDevice
from homeauto.house import register_sensor_event, register_motion_event
import logging
# This retrieves a Python logging instance (or creates it)
logger = logging.getLogger(__name__)

class VivintWirelessSensor(VivintDevice):
    """
    Generic Wireless Sensor.
    """

    """Generic state for all sensors they uses a simple boolean."""
    SENSOR_STATES = {True: "Opened", False: "Closed"}

    def __init__(self, device, root):
        super().__init__(device, root)

    def state(self):
        """Returns Opened or Closed based on the state of the sensor."""
        return self.SENSOR_STATES[super().get_device()[u"s"]]

    def update_device(self, updates):
        super().update_device(updates)
        name = super().get_device()[u"n"]
        logger.debug(name + " is now " + self.state())
        if "otion" in name:
            register_motion_event("Vivint", super().id())
        else:
            register_sensor_event("Vivint", super().id(), self.state())


