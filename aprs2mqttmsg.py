#!/usr/bin/python3

import argparse
import logging
import logging.handlers
import os
import re
import sys
import time

from aprs2mqtt import APRS2MQTT

if __name__ == "__main__":
    # get the options from the CLI
    ap = argparse.ArgumentParser(description="Send an APRS MSG va MQTT")
    ap.add_argument("--ssid", help="APRS SSID to send as", required=True)
    ap.add_argument("--to", help="APRS SSID to send to", required=True)
    ap.add_argument("--msg", help="the message (max 67 chars)", required=True)
    ap.add_argument("--broker", help="the MQTT broker FQDN or IP", required=True)
    ap.add_argument("--user", help="the username for the MQTT broker")
    ap.add_argument("--passwd", help="the password for the MQTT broker")
    ap.add_argument("--topic", help="the MQTT topic", required=True)
    ap.add_argument("--tls", help="use TLS for the MQTT connection", action="store_true")
    ap.add_argument("--debug", help="enable debug-level logging", action="store_true")
    args = ap.parse_args()

   
    log = logging.getLogger("aprs2mqttmsg")
    lh = logging.StreamHandler()
    lf = logging.Formatter(fmt='mqtt2aprsmsg: %(name)s: %(levelname)s: %(message)s')
    lh.setFormatter(lf)
    log.addHandler(lh)

    if args.debug:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.ERROR)

    try:
        log.debug("inside main try to setup client")

        usetls = False
        if args.tls:
            log.debug("using TLS due to --tls")
            usetls = True
        
        log.debug("get object for APRS2MQTT")
        a2m = APRS2MQTT.APRS2MQTT()
        a2m.log.addHandler(lh)

        if args.debug:
            a2m.log.setLevel(logging.DEBUG)
        else:
            a2m.log.setLevel(logging.ERROR)
        
        a2m.prep(str(args.broker), str(args.user), str(args.passwd), bool(usetls))
        log.debug("set topic")
        a2m.topic = args.topic
        
        a2mr = a2m.send_msg(args.ssid.upper(), args.to.upper(), args.msg)
        
        if a2mr is True:
            sys.exit(0)
        else:
            sys.exit(1)

    except KeyboardInterrupt:
        try:
            log.debug("exiting on interrupt")
            a2m.stop()
            sys.exit(0)
        except SystemExit:
            os._exit(0)

    except Exception as e:
        if str(e).find("getaddrinfo failed") > -1 or str(e).find("Errno -2") > -1:
            log.error("hostname not found; exiting")
            sys.exit("Error: unknown hostname")     
        log.error("quitting with general error: " + str(e))    
        sys.exit("Error: " + str(e))