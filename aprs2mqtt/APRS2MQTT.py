#!/usr/bin/python3

import logging
import logging.handlers
import os
import sys
import time

import paho.mqtt.client as mqtt

from .Util import APRS2MQTTUtil
from .Exceptions import (APRSMessageException, APRSPacketException,
                         ARPSSSIDException, APRS2MQTTExecption)

class APRS2MQTT:
    """
    Main class connecting to an MQTT broker to send APRS packages. 
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

    __error = False
    __errormsg = ""
    __published = False
    __ttime = 0

    # hostname for the MQTT broker   
    broker = None
    # password for the MQTT broker
    password = None
    # port for the MQTT broker, usually set to __MQTT_Port or __MQTT_TLS_Port but can be anything
    port = __MQTT_Port
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
        Set the initial connection information

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
        self.__MQTT_Client.on_publish = self.__on_publish      

    def __on_connect(self, client, userdata, flags, rc):
        """
        callback function used by paho.mqtt.client for connection events
        """
        self.log.debug("on_connect rc: " + mqtt.connack_string(rc))
        if rc != mqtt.CONNACK_ACCEPTED:
            self.log.error("could not connect to broker: " + mqtt.connack_string(rc))
            sys.exit(mqtt.connack_string(rc))

    def __on_publish(self, client, userdata, message):
        """
        callback function used by paho.mqtt.client for publish events. In this
        class it writes a message to the MQTT broker
        """
        self.published = True
    
    def __timer(self):
        self.__ttime += 100
        time.sleep(0.1)

    def __timeout(self):
        if self.__ttime > 2000:
            self.error = True
            self.errormsg = "timeout"
            return True
        else:
            return False

    def __raise_error(self, errmsg):
        self.log.error(errmsg)
        raise APRS2MQTTExecption(errmsg)
    
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

        self.log.debug("starting connect()")
        self.__MQTT_Client.connect(self.broker, self.port, self.__MQTT_Keepalive)

    def loop_start(self):
        """
        Execute the non-blocking listener

        If using send_msg() you don't need to call this first
        """
        self.log.debug("starting loop_start()")
        self.__MQTT_Client.loop_start()

    def send_msg(self, sendfrom, sendto, message):
        if not APRS2MQTTUtil.aprs_ssid_is_valid(sendfrom.upper()):
            raise ARPSSSIDException("invalid sending callsign: " + sendfrom.upper())

        if not APRS2MQTTUtil.aprs_ssid_is_valid(sendto.upper()):
            raise ARPSSSIDException("invalid recipient callsign: " + sendto.upper())

        if len(message) > 67:
            raise APRSMessageException("message body too long (max 67)")

        self.log.debug("start and loop_start")
        self.start()
        self.loop_start()
        self.log.debug("paho.mqtt publish")
        self.__MQTT_Client.publish(
            self.topic,
            sendfrom.upper() + ":" + sendto.upper() + ":" + message,
            qos=2
            )
        
        self.log.debug("waiting for state...")
        while not self.__published and not self.__error and not self.__timeout():
            self.log.debug("waiting for state...")
            self.__timer()

        self.stop()

        if self.__error is True:
            self.__raise_error("exiting with error: " + self.__errormsg)
        
        self.log.debug("exiting with success!")
        return True

    def stop(self):
        """
        stop the MQTT loop process

         If using send_msg() you don't need to call this first
        """
        self.log.info("disconnecting from {0:s}".format(self.broker))
        return self.__MQTT_Client.disconnect()
        