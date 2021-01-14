from pyvivintsky.vivint_device import VivintDevice


class VivintCamera(VivintDevice):
    """Represents a Vivint camera."""

    def __init__(self, device, root):
        super().__init__(device, root)

    async def get_direct_rtsp_url(self, hd: bool = False) -> str:
        """Return the direct rtsp url for this camera (in HD if requested), if any."""
        return (
            f"rtsp://{self.get_device()[u'un']}:{self.get_device()[u'pswd']}@{self.get_device()[u'caip']}:{self.get_device()[u'cap']}/{self.get_device()[u'cdp' if hd else u'cdps']}"
            if self.get_device()["cda"]
            else None
        )

    async def get_internal_rtsp_url(self, hd: bool = False) -> str:
        """Return the internal rtsp url for this camera (in HD if requested)."""
        return await self.get_rtsp_url(True, hd)

    async def get_external_rtsp_url(self, hd: bool = False) -> str:
        """Return the external rtsp url for this camera (in HD if requested)."""
        return await self.get_rtsp_url(False, hd)

    async def get_rtsp_url(self, internal: bool = False, hd: bool = False) -> str:
        """Return the requested rtsp url for this camera."""
        credentials = await self.get_root().get_panel_credentials()
        url = self.get_device()[f"c{'i' if internal else 'e'}u{'' if hd else 's'}"][0]
        return f"{url[:7]}{credentials[u'n']}:{credentials[u'pswd']}@{url[7:]}"
