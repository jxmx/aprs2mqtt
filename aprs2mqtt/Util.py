import re

class APRS2MQTTUtil:

    @staticmethod
    def aprs_ssid_is_valid(ssid):  
        """
        validate the SSID in an APRS packet is valid

        :param str callsign: an APRS callsign/ssid
        """

        segs = ssid.split("-")

        csre = r"^[A-Z0-9]{3,6}$"

        if len(segs) == 1:
            if re.search(csre, segs[0].upper()):
                return True
            else:
                return False

        elif len(segs) == 2:
            if re.search(csre, segs[0].upper()):
                if re.search(r"^[0-9]{1,2}$", segs[1]):
                    if 9 < int(segs[1]) < 16:
                        return True
                    elif re.search(r"^[0-9]$", segs[1]):
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False

    @staticmethod
    def create_aprs_msg_packet(fromssid, tossid, message, devid, path):
        """
        Write out an APRS MSG packet ready for AX.25 sending.
        """
        return str("{0:s}>{3:s},{4:s}::{1:s}:{2:s}".format(
            fromssid.upper(),
            tossid.upper().ljust(9),
            message,
            devid,
            path
            ))