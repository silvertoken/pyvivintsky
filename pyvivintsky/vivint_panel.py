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
        self.__system = self.__get_system()
        self.__childDevices = []

    def __get_system(self):
        return self.__vivintapi.getSystemInfo(str(self.__descriptor[u"panid"]))

    def id(self):
        return self.__system[u"system"][u"panid"]

    def getArmedState(self):
        """Return panels armed state."""
        return self.ARM_STATES[self.__descriptor[u"par"][0][u"s"]]

    def street(self):
        """Return the panels street address."""
        return self.__system[u"system"][u"add"]

    def zipCode(self):
        """Return the panels zip code."""
        return self.__system[u"system"][u"poc"]

    def city(self):
        """Return the panels city."""
        return self.__system[u"system"][u"cit"]

    def climateState(self):
        """Return the climate state"""
        return self.__system[u"system"][u"csce"]

    def pollDevices(self):
        """
        Poll all devices attached to this panel.
        """
        self.__system = self.__get_system()
        deviceDict = dict(
            [(d[u"_id"], d) for d in self.__system[u"system"][u"par"][0][u"d"]]
        )
        for device in self.__childDevices:
            device.updateJson(deviceDict[device.id()])

    def getDevices(self):
        """
        Return a list of all devices
        """
        devices = [
            self.getDeviceClass(device[u"t"])(device, self)
            for device in self.__system[u"system"][u"par"][0][u"d"]
        ]

        self.__childDevices = devices
        return self.__childDevices

    @staticmethod
    def getDeviceClass(typeString):
        mapping = {VivintDevice.DEVICE_TYPE_WIRELESS_SENSOR: VivintWirelessSensor}
        return mapping.get(typeString, VivintUnknownDevice)

