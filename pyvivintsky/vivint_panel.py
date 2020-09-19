import asyncio
from homeauto.api_vivint.pyvivintsky.vivint_device import VivintDevice
from homeauto.api_vivint.pyvivintsky.vivint_api import VivintAPI
from homeauto.api_vivint.pyvivintsky.vivint_wireless_sensor import VivintWirelessSensor
from homeauto.api_vivint.pyvivintsky.vivint_door_lock import VivintDoorLock
from homeauto.api_vivint.pyvivintsky.vivint_unknown_device import VivintUnknownDevice
from homeauto.house import RegisterSecurityEvent
import logging
# This retrieves a Python logging instance (or creates it)
logger = logging.getLogger(__name__)

class VivintPanel(VivintDevice):
    """
    Represents the main Vivint panel device
    """

    """
    states 1 and 2 come from panels
    """
    ARM_STATES = {0: "disarmed", 1: "armed_away", 2: "armed_stay", 3: "armed_stay", 4: "armed_away"}

    def __init__(self, vivintapi: VivintAPI, descriptor: dict, panel: dict):
        self.__vivintapi: VivintAPI = vivintapi
        self.__descriptor = descriptor
        self.__panel = panel
        self.__child_devices = self.__init_devices()

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

    async def poll_devices(self):
        """
        Poll all devices attached to this panel.
        """
        self.__panel = await self.__vivintapi.get_system_info(self.id())

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

    def handle_armed_message(self, message):
        logger.debug(message[u"da"][u"seca"][u"n"]+" set system "+self.ARM_STATES[message[u"da"][u"seca"][u"s"]])
        RegisterSecurityEvent(message[u"da"][u"seca"][u"n"],self.ARM_STATES[message[u"da"][u"seca"][u"s"]])

    def handle_disarmed_message(self, message):
        logger.debug(message[u"da"][u"secd"][u"n"]+" set system "+self.ARM_STATES[message[u"da"][u"secd"][u"s"]])
        RegisterSecurityEvent(message[u"da"][u"secd"][u"n"],self.ARM_STATES[message[u"da"][u"secd"][u"s"]])

    @staticmethod
    def get_device_class(type_string):
        mapping = {
            VivintDevice.DEVICE_TYPE_WIRELESS_SENSOR: VivintWirelessSensor,
            VivintDevice.DEVICE_TYPE_DOOR_LOCK: VivintDoorLock
        }
        return mapping.get(type_string, VivintUnknownDevice)

