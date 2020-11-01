#!/usr/bin/python3

import argparse
import logging
import logging.handlers
import os
import re
import sys
import time

from aprs2mqtt import MQTT2APRS

def main():
    # get the options from the CLI
    ap = argparse.ArgumentParser(description="Listen to MQTT for APRS MSGs to send")
    ap.add_argument("--broker", help="the MQTT broker FQDN or IP", required=True)
    ap.add_argument("--user", help="the username for the MQTT broker")
    ap.add_argument("--passwd", help="the password for the MQTT broker")
    ap.add_argument("--topic", help="the MQTT topic", required=True)
    ap.add_argument("--tls", help="use TLS for the MQTT connection", action="store_true")
    ap.add_argument("--queuedir",
        help="path to the KISS message queue (default=/var/aprs/queue)",
        default="/var/aprs/queue",
    )
    ap.add_argument("--debug", help="enable debug-level logging in syslog", action="store_true")
    args = ap.parse_args()

    # setup logging
    log = logging.getLogger("mqtt2aprsmsg")
    lh = logging.handlers.SysLogHandler(address = "/dev/log", facility="daemon")
    lf = logging.Formatter(fmt='mqtt2aprsmsg: %(name)s: %(levelname)s: %(message)s')
    lh.setFormatter(lf)
    log.addHandler(lh)

    if args.debug:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.INFO)

    try:
        log.debug("inside main try to setup client")

        usetls = False
        if args.tls:
            log.debug("using TLS due to --tls")
            usetls = True
        
        log.debug("get object for MQTT2APRS")
        m2a = MQTT2APRS.MQTT2APRS()
        m2a.log.addHandler(lh)

        if args.debug:
            m2a.log.setLevel(logging.DEBUG)
        else:
            m2a.log.setLevel(logging.INFO)
            
        m2a.prep(str(args.broker), str(args.user), str(args.passwd), bool(usetls))
        log.debug("set queudir if set")
        if args.queuedir is not None:
            m2a.queuedir = args.queuedir
        
        log.debug("set topic")
        m2a.topic = args.topic
        log.debug("start()")
        m2a.start()
        log.debug("loop()")
        m2a.loop()

    except KeyboardInterrupt:
        try:
            log.debug("exiting on interrupt")
            m2a.stop()
            sys.exit(0)
        except SystemExit:
            os._exit(0)

    except Exception as e:

        if str(e).find("getaddrinfo failed") > -1 or str(e).find("Errno -2") > -1:
            log.error("hostname not found; exiting")
            sys.exit("Error: unknown hostname")     
        log.error("quitting with general error: " + str(e))    
        sys.exit("Error: " + str(e))

if __name__ == "__main__":
    main()
