from pyvivintsky.vivint_api import VivintAPI
from pyvivintsky.vivint_panel import VivintPanel


class VivintSky:
    """Class to handle all communication with Vivint"""

    def __init__(self, username: str, password: str):
        self.__vivintApi = VivintAPI(username, password)
        self.__authData: dict = None

    def connect(self) -> None:
        """Connect to Vivint Sky"""
        if self.__vivintApi.login():
            self.__authData = self.__vivintApi.getAuthorizedUser()
        else:
            raise ("Failed to authenticate to Vivint Sky")

    def getPanels(self):
        """
        Return all panels the account has access too.
        """
        return [
            VivintPanel(self.__vivintApi, panel)
            for panel in self.__authData[u"u"][u"system"]
        ]

    def getPanelInfo(self, panelId):
        """Return the JSON data for the system"""
        return self.__vivintApi.getSystemInfo(panelId)

