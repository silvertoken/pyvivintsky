import requests
import json
import logging

VIVENT_API_ENDPOINT = "https://www.vivintsky.com/api/"

_LOGGER = logging.getLogger(__name__)


class VivintAPI:
    """Class to communicate with Vivint Sky API."""

    def __init__(self, username: str, password: str):
        self.__credentials = {"username": username, "password": password}
        self.__sessionId = None

    def login(self):
        """Performs login to Vivint API and stores session cookie."""
        response = requests.post(
            url=VIVENT_API_ENDPOINT + "login", json=self.__credentials
        )
        if not response.ok:
            response.raise_for_status()
        self.__sessionId = response.cookies["s"]
        return response.json()

    def getSystemInfo(self, panelId) -> dict:
        """Returns the the system info from the Vivint API."""
        if self.__sessionId == None:
            raise NameError(
                "You must login to the API first by calling the login method"
            )

        cookie = dict(s=self.__sessionId)
        response = requests.get(
            url=VIVENT_API_ENDPOINT + "systems/" + panelId, cookies=cookie
        )

        """Check for session timeout and relogin"""
        if response.status_code == 401:
            if login():
                cookie = dict(s=self.__sessionId)
                response = requests.get(
                    url=VIVENT_API_ENDPOINT + "systems/" + panelId, cookies=cookie,
                )

        if not response.ok:
            response.raise_for_status()

        return response.json()

