import aiohttp
import asyncio
import json

VIVENT_API_ENDPOINT = "https://www.vivintsky.com/api/"


class VivintAPI:
    """Class to communicate with Vivint Sky API."""

    def __init__(self, username: str, password: str):
        self.__credentials = {"username": username, "password": password}
        self.__session = None

    def get_session(self):
        return self.__session

    async def login(self):
        """Performs login to Vivint API and stores session cookie."""

        async with aiohttp.ClientSession() as session:
            async with session.post(
                url=VIVENT_API_ENDPOINT + "login", json=self.__credentials
            ) as response:
                if response.status == 200:
                    self.__session = response.cookies["s"]
                else:
                    response.raise_for_status()
                    return False
                return True

    async def get_system_info(self, panel_id):
        """Returns the system info from the Vivint API."""
        cookie = dict(s=self.__session.value)
        async with aiohttp.ClientSession(cookies=cookie) as session:
            async with session.get(
                url=VIVENT_API_ENDPOINT + "systems/" + panel_id
            ) as response:

                if response.status == 200:
                    return await response.json()
                else:
                    response.raise_for_status()
                    return None

    async def get_authorized_user(self):
        """Retuns the authorized user data from the Vivint API."""
        cookie = dict(s=self.__session.value)
        async with aiohttp.ClientSession(cookies=cookie) as session:
            async with session.get(url=VIVENT_API_ENDPOINT + "authuser") as response:
                if response.status == 200:
                    return await response.json()
                else:
                    response.raise_for_status()
                    return None

