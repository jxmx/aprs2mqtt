#!/usr/bin/pyton3

import logging
import logging.handlers
import os
import sys
import time

import paho.mqtt.client as mqtt

from .Util import APRS2MQTTUtil
from .Exceptions import (APRSMessageException, APRSPacketException,
                         ARPSSSIDException, MQTT2APRSExecption)

class MQTT2APRS:
    """
    Main class for managing connections with an MQTT broker and 
    digipeating messages to a KISS client. Currently this expects
    to write APRS packets directly to a filesystem location that
    has a KISS poller watching it (e.g. kissutil from direwolf).
    Eventually this class will be expanded to be its own KISS client
    directly
    """

    # this class' instance of a paho.mqtt.client object
    __MQTT_Client = mqtt.Client()
    # MQTT keepalive timer
    __MQTT_Keepalive = 60
    # standard non-TLS MQTT port
    __MQTT_Port = 1883
    # standard TLS MQTT port
    __MQTT_TLS_Port = 8883

    # log
    log = None

    # hostname for the MQTT broker   
    broker = None
    # device ID code for the APRS packet - see http://aprs.org/aprs11/tocalls.txt
    devid = "APN000"
    # APRS path to set in the packet
    path = "WIDE2-2"
    # password for the MQTT broker
    password = None
    # port for the MQTT broker, usually set to __MQTT_Port or __MQTT_TLS_Port but can be anything
    port = __MQTT_Port
    # directory where the ARPS KISS poller is watching for packets
    queuedir = "/var/aprs/queue"
    # MQTT topic(s) to list for. Supports the full MQTTv3 filtering syntax
    topic = None
    # Toggles the use of TLS for the MQTT broker
    use_tls = False
    # username for the MQTT broker
    username = None

    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.log.addHandler(logging.NullHandler())
        
    def prep(self, broker, username, password, tls):
        """
        set the connection information

        :param str broker: FQDN or IP address of the MQTT broker (required for connecting)
        :username str broker: username to connect the MQTT broker (optional for connecting)
        :password str broker: password to connect to the MQTT broker (optional for connecting)
        :param bool tls: 
        """
        
        if tls is True:
            self.log.debug("using tls")
            self.port = self.__MQTT_TLS_Port
            self.__MQTT_Client.tls_set()

        if username is not None:
            self.log.debug("using username " + username)
            self.username = username
        
            if password is not None:
                self.log.debug("using password specified")
                self.password = password
        
            self.__MQTT_Client.username_pw_set(self.username, self.password)

        self.log.debug("using broker " + broker)
        self.broker = broker

        self.__MQTT_Client.on_connect = self.__on_connect
        self.__MQTT_Client.on_message = self.__on_message      

    def __on_connect(self, client, userdata, flags, rc):
        """
        callback function used by paho.mqtt.client for connection events
        """
        self.log.debug("on_connect rc: " + mqtt.connack_string(rc))
        if rc != mqtt.CONNACK_ACCEPTED:
            self.log.error("could not connect to broker: " + mqtt.connack_string(rc))
            sys.exit(mqtt.connack_string(rc))
        else:
            if self.topic is not None:
                self.log.debug("on_connect subscribe: " + self.topic)
                self.__MQTT_Client.subscribe(self.topic)

    def __on_message(self, client, userdata, message):
        """
        callback function used by paho.mqtt.client for message events. In this
        class it writes the MQTT message to the ARPS KISS queue dir
        """
        self.log.debug("on_message with message: " + message.payload.decode('utf-8'))
        aprsmsgs = message.payload.decode('utf-8').split(":", 2)
        
        if len(aprsmsgs) == 3:
            try:
                if not APRS2MQTTUtil.aprs_ssid_is_valid(aprsmsgs[0].upper()):
                    raise ARPSSSIDException("invalid sending callsign: " + aprsmsgs[0].upper())

                if not APRS2MQTTUtil.aprs_ssid_is_valid(aprsmsgs[1].upper()):
                    raise ARPSSSIDException("invalid recipient callsign: " + aprsmsgs[1].upper())

                if len(aprsmsgs[2]) > 67:
                    raise APRSMessageException("message body too long (max 67)")

                m = APRS2MQTTUtil.create_aprs_msg_packet(
                    aprsmsgs[0].upper(),
                    aprsmsgs[1].upper(),
                    aprsmsgs[2],
                    self.devid,
                    self.path
                )
                f = open(os.path.join(self.queuedir,str(time.time_ns())), "w")
                self.log.info("sending >> {0:s}".format(m))
                f.write(m)
                f.close()
            except Exception as e:
                self.log.info("ignoring message with invalid item: " + str(e))

        else:
            self.log.info("ignoring invalid message format: " + message.payload.decode('utf-8'))

    def __raise_error(self, errmsg):
        self.log.error(errmsg)
        raise MQTT2APRSExecption(errmsg)
    
    def start(self):
        """
        start the MQTT instance

        note: this has no return as any activity and errors are handled by the
        __on_connect callback but all operations starting from here
        and through the rest of a logical flow of this modules
        should be called from a try/raise block
        """
        if self.broker is None:
            self.__raise_error("broker not set for {__name__}.broker; cannot start")

        if self.topic is None:
            self.__raise_error("topic not set for {__name__}.topic; cannot start")

        self.log.info("connecting to broker {0:s}:{1:s} and listening to {2:s}".format(
            self.broker, str(self.port), self.topic))

        self.__MQTT_Client.connect(self.broker, self.port, self.__MQTT_Keepalive)
 
    def loop(self):
        """
        Execute the blocking listener. This method does not exit because it calls
        a blocking method for the listening thread. To leave this method,
        the stop() method must be called from either a callback or a signal. Alternatively
        operate the paho.mqtt.client.loop* methods directly on the MQTT2ARPS.__MQTT_Client
        object in this class (recommended only for savvy MQTT and threading programmers)
        """
        self.log.debug("starting loop_forever()")
        self.__MQTT_Client.loop_forever()

    def stop(self):
        """
        stop the MQTT loop process
        """
        self.log.info("disconnecting from {0:s}".format(self.broker))
        return self.__MQTT_Client.disconnect()
        