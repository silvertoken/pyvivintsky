import logging
from enum import Enum

from pyvivintsky.vivint_api import VivintAPI
from pyvivintsky.vivint_camera import VivintCamera
from pyvivintsky.vivint_device import VivintDevice
from pyvivintsky.vivint_door_lock import VivintDoorLock
from pyvivintsky.vivint_garage_door import VivintGarageDoor
from pyvivintsky.vivint_unknown_device import VivintUnknownDevice
from pyvivintsky.vivint_wireless_sensor import VivintWirelessSensor

logger = logging.getLogger(__name__)


class VivintPanel(VivintDevice):
    """Represents the main Vivint panel device."""

    class ArmState(Enum):
        DISARMED = 0
        ARMING_AWAY_IN_EXIT_DELAY = 1
        ARMING_STAY_IN_EXIT_DELAY = 2
        ARMED_STAY = 3
        ARMED_AWAY = 4
        ARMED_STAY_IN_ENTRY_DELAY = 5
        ARMED_AWAY_IN_ENTRY_DELAY = 6
        ALARM = 7
        ALARM_FIRE = 8
        DISABLED = 11
        WALK_TEST = 12

    def __init__(self, vivintapi: VivintAPI, descriptor: dict, system: dict):
        self.__vivintapi: VivintAPI = vivintapi
        self.__descriptor = descriptor
        self.__system = system
        self.__panel = None
        self.__child_devices = self.__init_devices()
        self.__credentials = None
        self._manufacturer = "Vivint"
        self._callback = None

    def __init_devices(self):
        """
        Initialize the devices
        """
        devices = {}
        for device in self.__system["par"][0]["d"]:
            devices[str(device["_id"])] = self.get_device_class(device["t"])(
                device, self
            )
            if device["t"] == "primary_touch_link_device":
                self.__panel = devices[str(device["_id"])]

        return devices

    def get_api(self):
        """Return the Vivint API."""
        return self.__vivintapi

    @property
    def id(self) -> str:
        """Return the id for this panel."""
        return str(self.__system.get("panid"))

    @property
    def serial_number(self) -> str:
        """Return the serial number for this panel."""
        return self.id

    @property
    def name(self):
        """Return the name of the panel."""
        return self.__descriptor.get("sn")

    @property
    def state(self):
        """Return the state of the panel."""
        return self.ArmState(self.__system.get("s"))

    @property
    def changed_by(self):
        """Return the name of the user that last changed the state of the system."""
        return self.__system.get(
            "secd" if self.state == self.ArmState.DISARMED else "seca"
        ).get("n")

    @property
    def software_version(self) -> str:
        """Return the software version of this device, if any."""
        return self.__panel.software_version

    @property
    def model(self):
        """Return the model (panel type) of this panel."""
        return "Sky Control" if self.__panel.get_device()["pant"] == 1 else "Smart Hub"

    @property
    def direct_ip(self):
        """Return  the panel's local ip address."""
        return self.__panel.get_device()["dip"]

    @property
    def street(self):
        """Return the panels street address."""
        return self.__system["add"]

    @property
    def zip_code(self):
        """Return the panels zip code."""
        return self.__system["poc"]

    @property
    def city(self):
        """Return the panels city."""
        return self.__system["cit"]

    @property
    def climate_state(self):
        """Return the climate state"""
        return self.__system["csce"]

    async def poll_devices(self):
        """Poll all devices attached to this panel."""
        self.__system = await self.__vivintapi.get_system_info(self.id)

    async def get_panel_credentials(self):
        """Gets the panel credentials."""
        if self.__credentials is None:
            self.__credentials = await self.__vivintapi.get_panel_credentials(self.id)
        return self.__credentials

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
                if key not in ignored_keys and key in self.__system.keys():
                    if type(message["da"][key]) is dict:
                        self.__system[key].update(message["da"][key])
                    else:
                        self.__system[key] = message["da"][key]

                if key in ["seca", "secd"]:
                    self.handle_arming_message(message["da"][key])

            self.callback()

    def handle_arming_message(self, message):
        logger.debug(message["n"] + " set system " + self.state.name)

    async def set_armed_state(self, arm_state: ArmState):
        """Sets the panels armed state."""
        await self.__vivintapi.set_armed_state(self.id, arm_state.value)

    @staticmethod
    def get_device_class(type_string):
        mapping = {
            VivintDevice.DEVICE_TYPE_WIRELESS_SENSOR: VivintWirelessSensor,
            VivintDevice.DEVICE_TYPE_DOOR_LOCK: VivintDoorLock,
            VivintDevice.DEVICE_TYPE_GARAGE_DOOR: VivintGarageDoor,
            VivintDevice.DEVICE_TYPE_CAMERA: VivintCamera,
        }
        return mapping.get(type_string, VivintUnknownDevice)
