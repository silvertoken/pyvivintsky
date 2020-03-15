from pyvivintsky.vivint_device import VivintDevice
from pyvivintsky.vivint_api import VivintAPI
from pyvivintsky.vivint_wireless_sensor import VivintWirelessSensor
from pyvivintsky.vivint_unknown_device import VivintUnknownDevice


class VivintPanel(VivintDevice):
    """
    Represents the main Vivint panel device
    """

    ARM_STATES = {0: "disarmed", 3: "armed_stay", 4: "armed_away"}

    def __init__(self, vivintapi, descriptor):
        self.__vivintapi: VivintAPI = vivintapi
        self.__descriptor = descriptor
        self.__panel = self.__init_panel()
        self.__child_devices = self.__init_devices()

    def __init_panel(self):
        return self.__vivintapi.get_system_info(str(self.__descriptor[u"panid"]))

    def __init_devices(self):
        """
        Initialize the devices
        """
        devices = {}
        for device in self.__panel[u"system"][u"par"][0][u"d"]:
            devices[str(device[u"_id"])] = self.get_device_class(device[u"t"])(
                device, self
            )
        return devices

    def id(self):
        return str(self.__panel[u"system"][u"panid"])

    def get_armed_state(self):
        """Return panels armed state."""
        return self.ARM_STATES[self.__descriptor[u"par"][0][u"s"]]

    def street(self):
        """Return the panels street address."""
        return self.__panel[u"system"][u"add"]

    def zip_code(self):
        """Return the panels zip code."""
        return self.__panel[u"system"][u"poc"]

    def city(self):
        """Return the panels city."""
        return self.__panel[u"system"][u"cit"]

    def climate_state(self):
        """Return the climate state"""
        return self.__panel[u"system"][u"csce"]

    def poll_devices(self):
        """
        Poll all devices attached to this panel.
        """
        self.__panel = self.__init_panel()

    def get_devices(self):
        """
        Returns the current list of devices attached to the panel.
        """
        return self.__child_devices

    def get_device(self, id):
        return self.__child_devices[id]

    def update_device(self, id, updates):
        self.__child_devices[id].update_device(updates)

    def handle_message(self, message):
        if u"d" in message[u"da"].keys():
            for msg_device in message[u"da"][u"d"]:
                self.update_device(str(msg_device[u"_id"]), msg_device)

    @staticmethod
    def get_device_class(type_string):
        mapping = {VivintDevice.DEVICE_TYPE_WIRELESS_SENSOR: VivintWirelessSensor}
        return mapping.get(type_string, VivintUnknownDevice)

