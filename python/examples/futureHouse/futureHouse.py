import sys
from Pubnub import Pubnub

publish_key = len(sys.argv) > 1 and sys.argv[1] or 'demo-36'
subscribe_key = len(sys.argv) > 2 and sys.argv[2] or 'demo-36'
secret_key = len(sys.argv) > 3 and sys.argv[3] or 'demo-36'
cipher_key = len(sys.argv) > 4 and sys.argv[4] or ''
ssl_on = len(sys.argv) > 5 and bool(sys.argv[5]) or False

## -----------------------------------------------------------------------
## Initiate Pubnub State
## -----------------------------------------------------------------------
pubnub = Pubnub(publish_key=publish_key, subscribe_key=subscribe_key,
                secret_key=secret_key, cipher_key=cipher_key, ssl_on=ssl_on)

channel = 'futureHouse'


# Asynchronous usage
def callback(message, channel):
    print(message)


def error(message):
    print("ERROR : " + str(message))


def connect(message):
    print("CONNECTED")


def reconnect(message):
    print("RECONNECTED")


def disconnect(message):
    print("DISCONNECTED")


pubnub.subscribe(channel, callback=callback, error=callback,
                 connect=connect, reconnect=reconnect, disconnect=disconnect)