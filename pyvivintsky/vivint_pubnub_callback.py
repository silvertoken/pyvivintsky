from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNOperationType, PNStatusCategory


class VivintPubNubCallback(SubscribeCallback):
    """
    Basic PubNub Callback to pass messages to the handler
    """

    def __init__(self, handler, connected, disconnected):
        self.__handler = handler
        self.__connected = connected
        self.__disconnected = disconnected

    def status(self, pubnub, status):

        # The status object returned is always related to subscribe but could contain
        # information about subscribe, heartbeat, or errors
        # use the operationType to switch on different options
        if (
            status.operation == PNOperationType.PNSubscribeOperation
            or status.operation == PNOperationType.PNUnsubscribeOperation
        ):
            if status.category == PNStatusCategory.PNConnectedCategory:
                """Fire off connected event"""
                self.__connected()
                # pass
                # This is expected for a subscribe, this means there is no error or issue whatsoever
            elif status.category == PNStatusCategory.PNReconnectedCategory:
                pass
                # This usually occurs if subscribe temporarily fails but reconnects. This means
                # there was an error but there is no longer any issue
            elif status.category == PNStatusCategory.PNDisconnectedCategory:
                print("Disconnect Event")
                # self.__disconnected()
                # pass
                # This is the expected category for an unsubscribe. This means there
                # was no error in unsubscribing from everything
            elif status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
                print("PNUnexpectedDisconnectCategory")
                pass
                # This is usually an issue with the internet connection, this is an error, handle
                # appropriately retry will be called automatically
            elif status.category == PNStatusCategory.PNAccessDeniedCategory:
                pass
                # This means that PAM does not allow this client to subscribe to this
                # channel and channel group configuration. This is another explicit error
            elif status.category == PNStatusCategory.PNAcknowledgmentCategory:
                """
                Disconnected Category doesn't seem to fire.
                It insteads fires and acknowledgement category
                """
                if status.operation == PNOperationType.PNUnsubscribeOperation:
                    # print(status.is_error())
                    self.__disconnected()
            else:
                print("Category: " + str(status.category))
                # This is usually an issue with the internet connection, this is an error, handle appropriately
                # retry will be called automatically
        elif status.operation == PNOperationType.PNHeartbeatOperation:
            # Heartbeat operations can in fact have errors, so it is important to check first for an error.
            # For more information on how to configure heartbeat notifications through the status
            # PNObjectEventListener callback, consult http://www.pubnub.com/docs/python/api-reference-configuration#configuration
            if status.is_error():
                print("Heartbeat Error")
                pass
                # There was an error with the heartbeat operation, handle here
            else:
                pass
                # Heartbeat operation was successful
        else:
            print("Unknown Status: " + str(status.operation))
            pass
            # Encountered unknown status type

    def presence(self, pubnub, presence):
        # print("Presence Event!")
        # print(presence)
        pass  # handle incoming presence data

    def message(self, pubnub, message):
        # handle incoming messages
        # print("message")
        # print(message.message)
        self.__handler(message.message)

    def signal(self, pubnub, signal):
        # print("signal")
        # print(signal.message)
        pass  # handle incoming signals

