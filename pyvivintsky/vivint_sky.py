from pyvivintsky.vivint_api import VivintAPI
from pyvivintsky.vivint_panel import VivintPanel
from apscheduler.schedulers.background import BackgroundScheduler
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pyvivintsky.vivint_pubnub_callback import VivintPubNubCallback

VIVINT_SUB_KEY = "sub-c-6fb03d68-6a78-11e2-ae8f-12313f022c90"


class VivintSky:
    """Class to handle all communication with Vivint"""

    def __init__(self, username: str, password: str, refresh: int = 1200):
        self.__vivint_api = VivintAPI(username, password)
        self.__auth_data: dict = None
        self.__panels: dict = None
        self.__refresh_period = refresh
        self.__refresh_scheduler = None
        self.__pubnub: PubNub = None
        self.__pubnub_listener = VivintPubNubCallback(
            self.__handle_pubnub_message,
            self.__handle_pubnub_connected,
            self.__handle_pubnub_disconnected,
        )
        self.__pubnub_config = PNConfiguration()
        self.__pubnub_config.ssl = True
        self.__pubnub_config.subscribe_key = VIVINT_SUB_KEY

    def __refresh_session(self):
        if self.__vivint_api.login():
            self.__auth_data = self.__vivint_api.get_authorized_user()
            print("Refreshed session with VivintSky API")
        else:
            raise ("Failed to authenticate to Vivint Sky")

    def connect(self):
        """
        Connect to Vivint Sky using a scheduler to refresh the auth token.
        """
        if self.__refresh_scheduler == None:
            self.__refresh_scheduler = BackgroundScheduler()
        else:
            if self.__refresh_scheduler.running:
                self.__refresh_scheduler.shutdown()
            self.__refresh_scheduler.remove_all_jobs()

        self.__refresh_scheduler.add_job(
            self.__refresh_session, "interval", seconds=self.__refresh_period
        )
        self.__refresh_scheduler.start()
        self.__refresh_session()
        self.__panels = self.___init_panels()
        self.__init_pubnub()

    def ___init_panels(self):
        """
        Initialize the panels from the Vivint Panel class.
        """
        panels = {}
        for panel in self.__auth_data[u"u"][u"system"]:
            panels[str(panel[u"panid"])] = VivintPanel(self.__vivint_api, panel)
        return panels

    def __init_pubnub(self):
        """
        Initialize and subscribe to PubNub
        """
        if self.__pubnub == None:
            self.__pubnub = PubNub(self.__pubnub_config)
        self.__pubnub.add_listener(self.__pubnub_listener)
        self.__pubnub.subscribe().channels(
            "PlatformChannel#" + self.__auth_data[u"u"][u"mbc"]
        ).execute()

    def __handle_pubnub_message(self, message):
        if u"da" in message.keys():
            self.__panels[str(message[u"panid"])].handle_message(message)

    def __handle_pubnub_connected(self):
        print("Connected to PubNub channel")

    def __handle_pubnub_disconnected(self):
        print("Disconnected from PubNub channel")
        self.__pubnub.remove_listener(self.__pubnub_listener)
        self.__pubnub.stop()

    def get_panels(self):
        return self.__panels

    def get_panel(self, id):
        return self.__panels[id]

    def disconnect(self):
        """
        This disconnects and shuts down everything.
        """
        self.__pubnub.unsubscribe_all()
        self.__refresh_scheduler.shutdown()
        self.__refresh_scheduler.remove_all_jobs()
