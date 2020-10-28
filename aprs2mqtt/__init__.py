import re

def aprs_ssid_is_valid(callsign):
        
    segs = callsign.split("-")

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
