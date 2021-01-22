import logging

from pyvivintsky.vivint_device import VivintDevice

logger = logging.getLogger(__name__)


# Some Vivint supported cameras may be connected directly to your local network
# and the Vivint API reports these as having direct access availiable (cda).
# Ping cameras (alpha_cs6022_camera_device) can be setup to connect to your own
# Wi-Fi via a complicated process involving removing and resetting the camera,
# initiating WPS on your Wi-Fi and the Ping camera, and then adding a new camera
# from the panel within a limited timeframe. The Ping camera, however, seems to
# still have a VPN connection with the panel that prevents direct access except
# on very rare occasions. As such, we want to skip this model from direct access.
SKIP_DIRECT = ["alpha_cs6022_camera_device"]


class VivintCamera(VivintDevice):
    """Represents a Vivint camera."""

    def __init__(self, device, root):
        super().__init__(device, root)
        self._manufacturer = self.get_device().get("act").split("_")[0].title()
        self._model = self.get_device().get("act").split("_")[1].upper()

    async def get_direct_rtsp_url(self, hd: bool = False) -> str:
        """Return the direct rtsp url for this camera, in HD if requested, if any."""
        return (
            f"rtsp://{self.get_device()[u'un']}:{self.get_device()[u'pswd']}@{self.get_device()[u'caip']}:{self.get_device()[u'cap']}/{self.get_device()[u'cdp' if hd else u'cdps']}"
            if self.get_device()["cda"]
            and self.get_device().get("act") not in SKIP_DIRECT
            else None
        )

    async def get_internal_rtsp_url(self, hd: bool = False) -> str:
        """Return the internal rtsp url (streamed through panel) for this camera, in HD if requested."""
        return await self.get_rtsp_url(True, hd)

    async def get_external_rtsp_url(self, hd: bool = False) -> str:
        """Return the external rtsp url for this camera, in HD if requested."""
        return await self.get_rtsp_url(False, hd)

    async def get_rtsp_url(self, internal: bool = False, hd: bool = False) -> str:
        """Return the requested rtsp url for this camera."""
        credentials = await self.get_root().get_panel_credentials()
        url = self.get_device()[f"c{'i' if internal else 'e'}u{'' if hd else 's'}"][0]
        return f"{url[:7]}{credentials[u'n']}:{credentials[u'pswd']}@{url[7:]}"

    def update_device(self, updates):
        super().update_device(updates)
        if updates.get("ctd"):
            logger.debug(f"{self.name} thumbnail last updated at {updates.get('ctd')}")
        else:
            logger.debug(f"{self.name} updated")
