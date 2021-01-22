import re
from datetime import datetime

import aiohttp

VIVINT_API_ENDPOINT = "https://www.vivintsky.com/api/"


class VivintAPI:
    """Class to communicate with Vivint Sky API."""

    def __init__(self, username: str, password: str):
        self.__credentials = {"username": username, "password": password}
        self.__session = None
        self.__zwave_device_info = {}

    def get_session(self):
        return self.__session

    def session_valid(self):
        session_date = datetime.strptime(
            self.__session["expires"], "%a, %d %b %Y %H:%M:%S %Z"
        )
        current_date = datetime.utcnow()
        if current_date < session_date:
            return True
        else:
            return False

    async def login(self):
        """Performs login to Vivint API and stores session cookie."""

        async with aiohttp.ClientSession() as session:
            async with session.post(
                url=f"{VIVINT_API_ENDPOINT}login", json=self.__credentials
            ) as response:
                if response.status == 200:
                    self.__session = response.cookies["s"]
                else:
                    response.raise_for_status()
                    return False
                return True

    async def get_system_info(self, panel_id):
        """Returns the system info from the Vivint API."""
        if self.session_valid() == False:
            await self.login()
        cookie = dict(s=self.__session.value)
        async with aiohttp.ClientSession(cookies=cookie) as session:
            async with session.get(
                url=f"{VIVINT_API_ENDPOINT}systems/{panel_id}",
                headers={"Accept-Encoding": "application/json"},
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    response.raise_for_status()
                    return None

    async def get_authorized_user(self):
        """Retuns the authorized user data from the Vivint API."""
        if self.session_valid() == False:
            await self.login()
        cookie = dict(s=self.__session.value)
        async with aiohttp.ClientSession(cookies=cookie) as session:
            async with session.get(url=f"{VIVINT_API_ENDPOINT}authuser") as response:
                if response.status == 200:
                    return await response.json()
                else:
                    response.raise_for_status()
                    return None

    async def set_armed_state(self, panel_id, arm_state):
        """Sets the panels armed state by invoking the Vivint API."""
        if self.session_valid() == False:
            await self.login()
        cookie = dict(s=self.__session.value)
        async with aiohttp.ClientSession(cookies=cookie) as session:
            async with session.put(
                url=f"{VIVINT_API_ENDPOINT}{panel_id}/0/armedstates",
                json={"armState": arm_state},
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    response.raise_for_status()
                    return None

    async def set_garage_door_state(self, panel_id, device_id, garage_state):
        """Sets the garage door state by invoking the Vivint API."""
        if self.session_valid() == False:
            await self.login()
        cookie = dict(s=self.__session.value)
        async with aiohttp.ClientSession(cookies=cookie) as session:
            async with session.put(
                url=f"{VIVINT_API_ENDPOINT}{panel_id}/0/door/{device_id}",
                json={"s": garage_state},
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    response.raise_for_status()
                    return None

    async def set_lock_state(self, panel_id, device_id, lock_state):
        """Sets the lock state by invoking the Vivint API."""
        if self.session_valid() == False:
            await self.login()
        cookie = dict(s=self.__session.value)
        async with aiohttp.ClientSession(cookies=cookie) as session:
            async with session.put(
                url=f"{VIVINT_API_ENDPOINT}{panel_id}/1/locks/{device_id}",
                json={"s": lock_state},
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    response.raise_for_status()
                    return None

    async def get_panel_credentials(self, panel_id):
        """Gets the panel credentials by invoking the Vivint API."""
        if self.session_valid() == False:
            await self.login()
        cookie = dict(s=self.__session.value)
        async with aiohttp.ClientSession(cookies=cookie) as session:
            async with session.get(
                url=f"{VIVINT_API_ENDPOINT}panel-login/{panel_id}"
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    response.raise_for_status()
                    return None

    async def get_zwave_details(self, manufacturer_id, product_id, product_type_id):
        """Gets the zwave details by looking up the details on the openzwave device database."""
        zwave_lookup = f"{manufacturer_id}:{product_id}:{product_type_id}"
        device_info = self.__zwave_device_info.get(zwave_lookup)
        if device_info is not None:
            return device_info

        async with aiohttp.ClientSession() as session:
            async with session.get(
                url=f"http://openzwave.net/device-database/{manufacturer_id}:{product_id}:{product_type_id}"
            ) as response:
                if response.status == 200:
                    text = await response.text()
                    d = re.search("<title>(.*)</title>", text, re.IGNORECASE)
                    result = self.__zwave_device_info[zwave_lookup] = d[1].split(" - ")
                    return result
                else:
                    response.raise_for_status()
                    return None
