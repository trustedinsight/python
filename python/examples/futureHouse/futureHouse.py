import sys
from Pubnub import Pubnub
from Adafruit_PWM_Servo_Driver import PWM
import time
import random

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



# http://www.raspberrypi.org/forums/viewtopic.php?f=37&t=32826

# Initialise the PWM device using the default address
pwm = PWM(0x40, debug=False)

ledMin = 150  # Min pulse length out of 4096
ledMax = 600  # Max pulse length out of 4096

def setServoPulse(channel, pulse):
    pulseLength = 1000000                   # 1,000,000 us per second
    pulseLength /= 60                       # 60 Hz
    print "%d us per period" % pulseLength
    pulseLength /= 4096                     # 12 bits of resolution
    print "%d us per bit" % pulseLength
    pulse *= 1000
    pulse /= pulseLength
    pwm.setPWM(channel, 0, pulse)

pwm.setPWMFreq(60)                        # Set frequency to 60 Hz
while (True):
    for x in range(0,6) :
        # Change speed of continuous servo on channel O
        pwm.setPWM(x, 0, ledMin)
        time.sleep(random.uniform(0.005,0.0001))
        pwm.setPWM(x, 0, ledMax)
        time.sleep(random.uniform(0.005,0.0001))

pubnub.subscribe(channel, callback=callback, error=callback,
                 connect=connect, reconnect=reconnect, disconnect=disconnect)
