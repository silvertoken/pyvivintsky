import requests
import json

VIVENT_API_ENDPOINT = "https://www.vivintsky.com/api/"


class VivintAPI:
    """Class to communicate with Vivint Sky API."""

    def __init__(self, username: str, password: str):
        self.__credentials = {"username": username, "password": password}
        self.__sessionId = None
        self.__sessionInfo = None
        self.__systemInfo = None
        self.__panelId = None

    def login(self) -> None:
        """Performs login to Vivint API and stores session cookie."""
        response = requests.post(
            url=VIVENT_API_ENDPOINT + "login", json=self.__credentials
        )
        if not response.status_code != 200:
            response.raise_for_status()
        self.__sessionId = response.cookies["s"]
        self.__sessionInfo = response.json()
        self.__panelId = self.__sessionInfo[u"u"][u"system"][0][u"panid"]

    def updateSystemInfo(self) -> None:
        """Updates the system info from the Vivint API."""
        cookie = dict(s=self.__sessionId)
        response = requests.get(
            url=VIVENT_API_ENDPOINT + "systems/" + str(self.__panelId), cookies=cookie
        )
        if not response.status_code != 200:
            response.raise_for_status()
        self.__systemInfo = response.json()

    def getSystemInfo(self) -> None:
        """Returns the the system info from the Vivint API."""
        if self.__systemInfo == None:
            self.updateSystemInfo()
        return self.__systemInfo
