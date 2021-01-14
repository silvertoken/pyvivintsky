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
    def id(self) -> str:
        """Return the id for this device."""
        return str(self.__device.get("_id"))

    @property
    def serial_number(self) -> str:
        """Return the serial number for this device."""
        # wireless sensors and keyfobs
        serial_number = self.__device.get("ser")
        # glance panel
        panel_mac = self.__device.get("pmac")
        # cameras
        camera_mac = self.__device.get("cmac")

        return f"{self.__device.get(u'panid')}-{serial_number or panel_mac or camera_mac or self.id}"

    @property
    def name(self) -> str:
        return self.__device.get("n")

    @property
    def device_type(self) -> str:
        return self.__device["t"]

    @property
    def battery_level(self) -> int:
        """Return the battery level of this device, if any."""
        battery_level = self.__device.get("bl")
        low_battery = self.__device.get("lb")
        if battery_level is None and low_battery is None:
            return None
        elif battery_level is not None:
            return battery_level
        else:
            return 0 if low_battery else 100

    @property
    def software_version(self) -> str:
        """Return the software version of this device, if any."""
        # panels
        current_software_version = self.__device.get("csv")
        # cameras
        software_version = self.__device.get("sv")
        # z-wave devices (some)
        firmware_version = (
            ".".join([str(i) for s in self.__device.get("fwv") or [] for i in s])
            or None
        )
        # wireless sensors
        sensor_firmware_version = self.__device.get("sensor_firmware_version")
        return (
            current_software_version
            or software_version
            or firmware_version
            or sensor_firmware_version
        )

    def set_device(self, device) -> None:
        self.__device = device

    def update_device(self, updates) -> None:
        self.__device.update(updates)
        self.callback()

    def callback(self) -> None:
        if self._callback is not None:
            self._callback()
