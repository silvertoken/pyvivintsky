import requests
import json

VIVENT_API_ENDPOINT = "https://www.vivintsky.com/api/"


class VivintAPI:
    """Class to communicate with Vivint Sky API."""

    def __init__(self, username: str, password: str):
        self.__credentials = {"username": username, "password": password}
        self.__session_id = None

    def login(self):
        """Performs login to Vivint API and stores session cookie."""
        response = requests.post(
            url=VIVENT_API_ENDPOINT + "login", json=self.__credentials
        )
        if not response.ok:
            response.raise_for_status()
        self.__session_id = response.cookies["s"]
        return True

    def get_system_info(self, panel_id):
        """Returns the system info from the Vivint API."""
        if self.__session_id == None:
            raise NameError(
                "You must login to the API first by calling the login method"
            )

        cookie = dict(s=self.__session_id)
        response = requests.get(
            url=VIVENT_API_ENDPOINT + "systems/" + panel_id, cookies=cookie
        )

        if not response.ok:
            response.raise_for_status()

        return response.json()

    def get_authorized_user(self):
        """Retuns the authorized user data from the Vivint API."""
        if self.__session_id == None:
            raise NameError(
                "You must login to the API first by calling the login method"
            )

        cookie = dict(s=self.__session_id)
        response = requests.get(url=VIVENT_API_ENDPOINT + "authuser", cookies=cookie)

        if not response.ok:
            response.raise_for_status()

        return response.json()

