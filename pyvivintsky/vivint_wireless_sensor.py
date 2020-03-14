from pyvivintsky.vivint_device import VivintDevice


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
        print(super().get_device()[u"n"] + " is now " + self.state())
