class APRSMessageException(Exception):
    """
    raise when a message payload in a a Message fails validation (usually length)
    """
    pass

class APRSPacketException(Exception):
    """
    raise when a package is requested but the object is not complete/correct
    """
    pass

class ARPSSSIDException(Exception):
    """
    raised when an APRS SSID/callsign fails validation
    """
    pass

class MQTT2APRSExecption(Exception):
    """
    raised when an MQTT operation in MQTT2APRS failes or is invalid
    """
    pass