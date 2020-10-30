# aprs2mqtt

This project is a collection of various utilities to interface
APRS with MQTT.

- Python Module aprs2mqtt
- aprs2mqttmsg - send an APRS message into the MQTT broker
- mqtt2arpsmsg - receive an APRS message from the MQTT broker and inject to KISS queue

## Installation

Still working on a PyPi installer. At the moment manual install is easiest.

The quickest way to get started is to simply download the latest release 
or do a 'git clone' of this repository on the latest release branch. Use
everything from the cloned/downloaded directory.

If you want something more production ready:
1. Download or 'git clone' the latest release
2. Copy the contents of ./aprs2mqtt into a reasonable location found in your Python sys.path
3. Copy the direct commands somewhere in your $PATH or wherever you want to use them

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

