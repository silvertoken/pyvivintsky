from pyvivintsky.vivint_device import VivintDevice


class VivintWirelessSensor(VivintDevice):
    def __init__(self, json, root):
        super().__init__(json, root)

    def state(self):
        return self.__json[u"s"]
