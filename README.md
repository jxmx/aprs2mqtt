# aprs2mqtt

This project is a collection of various utilities to interface
APRS with MQTT.

- Python Module aprs2mqtt
- aprs2mqttmsg - send an APRS message into the MQTT broker
- mqtt2arpsmsg - receive an APRS message from the MQTT broker and inject to KISS queue

## Installation

aprs2mqtt is now available through PyPi as an installable package.

Installation can be done to any Python system with

    python -m pip install aprs2mqtt

On Linux and similar systems, the scripts will be installed in /usr/local/bin
or wherever you specify based on the pip install process. On Windows, this will
end up in your Scripts directory which should be in your path if setup correctly.

## Portability Note
aprs2mqttmsg and the Python packages/modules should be portable to all common 
platforms - Windows, Linux, MacOS, etc.. However mqtt2aprsmsg has some 
Linux/BSD-ish-ness to it and won't currently work (well) on Windows mostly because
it's built to work with Direwolf. True cross-platform is an eventual goal to interact 
with other KISS interfaces rather than just Direwolf/kissutil.

## Sending a Message

Use the aprs2mqttmsg command to send a message. Here is an example:

    python .\aprs2mqttmsg --broker mqtt.example.com --topic svc/aprs/msg/queue \
        --ssid CALLSIGN2-1 --to CALLSIGN2-1 --msg "Test Message"

Eventually I will document how to setup an MQTT broker for interacting with Direwolf for APRS
but this is not that day.

Many MQTT brokers will require a username and password and likely use TLS. You will need
to look at the help for the --user --passwd and --tls options

## Receiving Messages

This is more involved and currently assumes you are proficient in Linux, Direwolf, KISS
interfactes (this uses kissutil), and APRS. The gist of what to do is on your Direwolf/KISS
server run:

    ./mqtt2aprsmsg --broker mqtt.example --user=USER --passwd=PASSWD \
        --tls --topic svc/aprs/msg/queue --debug

You will have to adjust --user, --passwd, and --tls based on your MQTT setup but I highly
suggest using TLS and authentication for any MQTT server on the Internet. There is also
additional option --queuedir to change where the KISS queue is located (kissutil read directory).

## Starting mqtt2aprsmsg On Boot

The easiest way to launch mqtt2aprsmsg is through systemd. Put the following in
**/etc/systemd/system/mqtt2aprsmsg.service**:

    [Unit]
    Description=MQTT/APRS Interface Listener for MSG
    After=kissutil.service

    [Service]
    Type=simple
    ExecStart=/usr/local/bin/mqtt2aprsmsg --broker HOSTNAME --user=USER --passwd=PASS --tls --topic svc/aprs/msg/queue

    [Install]
    WantedBy=multi-user.target
