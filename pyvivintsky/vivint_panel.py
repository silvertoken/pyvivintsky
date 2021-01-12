import logging

from pyvivintsky.vivint_api import VivintAPI
from pyvivintsky.vivint_device import VivintDevice
from pyvivintsky.vivint_door_lock import VivintDoorLock
from pyvivintsky.vivint_unknown_device import VivintUnknownDevice
from pyvivintsky.vivint_wireless_sensor import VivintWirelessSensor

logger = logging.getLogger(__name__)


class VivintPanel(VivintDevice):
    """
    Represents the main Vivint panel device
    """

    ARM_STATES = {0: "disarmed", 3: "armed_stay", 4: "armed_away"}

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
        for device in self.__panel["system"]["par"][0]["d"]:
            devices[str(device["_id"])] = self.get_device_class(device["t"])(
                device, self
            )
        return devices

    def id(self):
        return str(self.__panel["system"]["panid"])

    def name(self):
        """Return the name of the panel."""
        return self.__descriptor["sn"]

    def get_armed_state(self):
        """Return panels armed state."""
        return self.ARM_STATES[self.__panel["system"]["s"]]

    def street(self):
        """Return the panels street address."""
        return self.__panel["system"]["add"]

    def zip_code(self):
        """Return the panels zip code."""
        return self.__panel["system"]["poc"]

    def city(self):
        """Return the panels city."""
        return self.__panel["system"]["cit"]

    def climate_state(self):
        """Return the climate state"""
        return self.__panel["system"]["csce"]

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
        if "d" in message["da"].keys():
            for msg_device in message["da"]["d"]:
                self.update_device(str(msg_device["_id"]), msg_device)
        else:
            ignored_keys = ["plctx"]

            for key in message["da"].keys():
                if key not in ignored_keys and key in self.__panel["system"].keys():
                    if type(message["da"][key]) is dict:
                        self.__panel["system"][key].update(message["da"][key])
                    else:
                        self.__panel["system"][key] = message["da"][key]

                if key in ["seca", "secd"]:
                    self.handle_arming_message(message["da"][key])

    def handle_arming_message(self, message):
        logger.debug(message["n"] + " set system " + self.ARM_STATES[message["s"]])

    async def set_armed_state(self, arm_state):
        """Sets the panels armed state."""
        await self.__vivintapi.set_armed_state(self.id(), arm_state)

    @staticmethod
    def get_device_class(type_string):
        mapping = {
            VivintDevice.DEVICE_TYPE_WIRELESS_SENSOR: VivintWirelessSensor,
            VivintDevice.DEVICE_TYPE_DOOR_LOCK: VivintDoorLock,
        }
        return mapping.get(type_string, VivintUnknownDevice)
