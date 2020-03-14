class VivintDevice(object):
    """
    Class for Vivint Devices
    """

    DEVICE_TYPE_TOUCH_PANEL = "primary_touch_link_device"
    DEVICE_TYPE_WIRELESS_SENSOR = "wireless_sensor"

    def __init__(self, device, root):
        self.__device = device
        self.__root = root

    def get_root(self):
        """ Return the root device this is attached too."""
        return self.__root

    def get_device(self):
        """ Returns the json dictionary data from the initial request."""
        return self.__device

    def id(self):
        return self.__device[u"_id"]

    def name(self):
        if u"n" in self.__device.keys():
            return self.__device[u"n"]
        else:
            return ""

    def device_type(self):
        return self.__device[u"t"]

    def set_device(self, device):
        self.__device = device

    def update_device(self, updates):
        self.__device.update(updates)
