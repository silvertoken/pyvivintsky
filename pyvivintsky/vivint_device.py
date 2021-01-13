from typing import Any, Dict


class VivintDevice(object):
    """Class for Vivint Devices"""

    DEVICE_TYPE_CAMERA = "camera_device"
    DEVICE_TYPE_DOOR_LOCK = "door_lock_device"
    DEVICE_TYPE_GARAGE_DOOR = "garage_door_device"
    DEVICE_TYPE_MULTILEVEL_SWITCH = "multilevel_switch_device"
    DEVICE_TYPE_TOUCH_PANEL = "primary_touch_link_device"
    DEVICE_TYPE_WIRELESS_SENSOR = "wireless_sensor"

    # Other device types seen but not yet implemented:
    # iot_service
    # keyfob_device
    # network_hosts_service
    # panel_diagnostics_service
    # phillips_hue_bridge_device
    # scheduler_service
    # slim_line_device
    # thermostat_device
    # yofi_device

    def __init__(self, device, root) -> None:
        self.__device = device
        self.__root = root
        self._callback = None

    def get_root(self) -> object:
        """ Return the root device this is attached too."""
        return self.__root

    def get_device(self) -> Dict[str, Any]:
        """ Returns the json dictionary data from the initial request."""
        return self.__device

    @property
    def id(self) -> int:
        return self.__device[u"_id"]

    @property
    def name(self) -> str:
        if u"n" in self.__device.keys():
            return self.__device[u"n"]
        else:
            return ""

    @property
    def device_type(self) -> str:
        return self.__device[u"t"]

    @property
    def battery_level(self) -> int:
        """Return the battery level of this device, if any."""
        battery_level = self.__device.get(u"bl")
        low_battery = self.__device.get(u"lb")
        if battery_level is None and low_battery is None:
            return None
        elif battery_level is not None:
            return battery_level
        else:
            return 0 if low_battery else 100

    @property
    def software_version(self) -> str:
        """Return the software version of this device, if any."""
        current_software_version = self.__device.get(u"csv")
        software_version = self.__device.get(u"sv")
        firmware_version = (
            ".".join([str(i) for s in self.__device.get(u"fwv") or [] for i in s])
            or None
        )
        sensor_firmware_version = self.__device.get(u"sensor_firmware_version")
        return (
            current_software_version  # panels
            or software_version  # cameras
            or firmware_version  # z-wave devices (some)
            or sensor_firmware_version  # wireless sensors
        )

    def set_device(self, device) -> None:
        self.__device = device

    def update_device(self, updates) -> None:
        self.__device.update(updates)
        self.callback()

    def callback(self) -> None:
        if self._callback is not None:
            self._callback()
