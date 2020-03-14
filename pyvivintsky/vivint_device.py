class VivintDevice(object):
    """
    Class for Vivint Devices
    """

    DEVICE_TYPE_TOUCH_PANEL = "primary_touch_link_device"
    DEVICE_TYPE_WIRELESS_SENSOR = "wireless_sensor"

    def __init__(self, json, root):
        self.__json = json
        self.__root = root

    def getRoot(self):
        """ Return the root device this is attached too."""
        return self.__root

    def getJson(self):
        """ Returns the json dictionary data from the initial request."""
        return self.__json

    def id(self):
        return self.__json[u"_id"]

    def name(self):
        return self.__json[u"n"]

    def deviceType(self):
        return self.__json[u"t"]

    def updateJson(self, json):
        self.__json = json
