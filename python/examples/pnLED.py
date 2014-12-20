from Pubnub import Pubnub
import RPi.GPIO as GPIO ## Import GPIO library

GPIO.setmode(GPIO.BOARD) ## Use board pin numbering
GPIO.setup(12, GPIO.OUT) ## Setup GPIO Pin 7 to OUT
GPIO.output(12,True) ## Turn on GPIO pin 7

pubnub = Pubnub(publish_key="demo-36", subscribe_key="demo-36", ssl_on=False)

# Listen for Messages

channel = 'rpi_1'

def callback(message, channel):
    print(message)

    if (message['command'] == "led_off"):
    	GPIO.output(12,False)
    elif (message['command'] == "led_on"):
    	GPIO.output(12,True)



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
