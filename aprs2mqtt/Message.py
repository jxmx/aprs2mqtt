from .Exceptions import (APRSMessageException, APRSPacketException,
                         ARPSSSIDException)
from .Util import APRS2MQTTUtil


class Message:
    """
    Class to hold and operate APRS Message packets
    """

    sendfrom = None
    sendto = None
    message = None
    path = "WIDE2-2"
    prg = "APN000"

    def __init__(self, sendfrom: str=None, sendto:str=None, message: str=None):
        self.sendfrom = sendfrom.upper()
        self.sendto = sendto.upper()
        self.message = message

    def getsendfrom(self):
        """
        returns a string of the from SSID
        """
        return self.sendfrom

    def setsendfrom(self, sendfrom):
        """
        set the from SSID
        
        :param str sendfrom: a valid APRS SSID

        returns True on success, rasises APRSSSIDException if bad SSID
        """
        if APRS2MQTTUtil.aprs_ssid_is_valid(sendfrom):
            self.sendfrom = sendfrom.upper()
            return True
        else:
            raise ARPSSSIDException("SSID is invalid")
    
    def getsendto(self):
        """
        returns a string of the to SSID
        """
        return self.sendto

    def setsentto(self, sendto):
        """
         set the to SSID
        :param str sendto: a valid APRS SSID

        returns True on success, rasises APRSSSIDException if bad SSID
        """
        if APRS2MQTTUtil.aprs_ssid_is_valid(sendto):
            self.sendto = sendto.upper()
            return True
        else:
            raise ARPSSSIDException("SSID is invalid")       

    def getmessage(self):
        """
        returns a string of the message
        """
        return self.message
    
    def setmessage(self, message):
        """
        set the message
        :param str message: the message
        
        returns True on success, raises APRSMessageException if the message is too long or otherwise invalid
        """
        if 0 < len(message) < 67:
            self.message = message
            return True
        else:
            raise APRSMessageException("message was not between 0 and 67 chars")

    def __isvalidmsg(self):
        """
        checks if a Message class is valid - i.e. ready to send
        Returns a True on success, raises an APRSSSIDException or
        APRSMessageException on failure
        """
        if not APRS2MQTTUtil.aprs_ssid_is_valid(self.sendfrom):
            raise ARPSSSIDException("from SSID is invalid")
        if not APRS2MQTTUtil.aprs_ssid_is_valid(self.sendto):
            raise ARPSSSIDException("to SSID is invalid")
        if self.message is None:
            raise APRSMessageException("message is empty")
        if len(self.message) > 67:
            raise APRSMessageException("message is longer than 67 characters")
        
        return True
    
    def getpacket(self):
        """
        returns the String of a complete ready-to-send APRS packet for a message
        raises APRSPacketException if the message is not complete/valid
        """
        if self.__isvalidmsg():
            # FROM>PRG,PATH::TO:MESSAGE
            return("{0:s}>{1:s},{2:s}::{3:s}:{4:s}".format(
                self.sendfrom,
                self.prg, 
                self.path,
                self.sendto.ljust(9),
                self.message
                ))
        else:
            raise APRSPacketException("the message packet is incomplete")
