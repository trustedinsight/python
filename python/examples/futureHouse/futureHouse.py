import sys
from Pubnub import Pubnub
from Adafruit_PWM_Servo_Driver import PWM
import time
import random
import Adafruit_BMP.BMP085 as BMP085
import Adafruit_DHT

sensor = BMP085.BMP085()

publish_key = len(sys.argv) > 1 and sys.argv[1] or 'demo-36'
subscribe_key = len(sys.argv) > 2 and sys.argv[2] or 'demo-36'
secret_key = len(sys.argv) > 3 and sys.argv[3] or 'demo-36'
cipher_key = len(sys.argv) > 4 and sys.argv[4] or ''
ssl_on = len(sys.argv) > 5 and bool(sys.argv[5]) or False

pubnub = Pubnub(publish_key=publish_key, subscribe_key=subscribe_key,
                secret_key=secret_key, cipher_key=cipher_key, ssl_on=ssl_on)

channel = 'futureHouse'

# pulse lengths have a max of 4096

leds = [
    {'name': 'iceCaveLamp', 'minPulseLength': 150, 'maxPulseLength': 2600, 'waitFloor': 0.0001, 'waitCeiling': 0.005},
    {'name': 'iceCaveCrystal', 'minPulseLength': 150, 'maxPulseLength': 2600, 'waitFloor': 0.0001, 'waitCeiling': 0.005},
    {'name': 'fireplaceOrange', 'minPulseLength': 150, 'maxPulseLength': 2600, 'waitFloor': 0.0001, 'waitCeiling': 0.005},
    {'name': 'campfire', 'minPulseLength': 150, 'maxPulseLength': 2600, 'waitFloor': 0.0001, 'waitCeiling': 0.005},
    {'name': 'porchLight', 'minPulseLength': 150, 'maxPulseLength': 2600, 'waitFloor': 0.0001, 'waitCeiling': 0.005},
    {'name': 'fireplaceRed', 'minPulseLength': 150, 'maxPulseLength': 2600, 'waitFloor': 0.0001, 'waitCeiling': 0.005},
    {'name': 'stove', 'minPulseLength': 150, 'maxPulseLength': 2600, 'waitFloor': 0.0001, 'waitCeiling': 0.005}
]




def callback(message, channel):

    # LED Setters
    if 'ledID' in message:
        if 'minPulseLength' in message:
            print "Setting minPulseLength to: " + str(message['minPulseLength'])
            leds[message['ledID']]['minPulseLength'] = message['minPulseLength']
        if 'maxPulseLength' in message:
            print "Setting maxPulseLength to: " + str(message['maxPulseLength'])
            leds[message['ledID']]['maxPulseLength'] = message['maxPulseLength']
        if 'waitCeiling' in message:
            print "Setting waitCeiling to: " + str(message['waitCeiling'])
            leds[message['ledID']]['waitCeiling'] = message['waitCeiling']
        if 'waitFloor' in message:
            print "Setting waitFloor to: " + str(message['waitFloor'])
            leds[message['ledID']]['waitFloor'] = message['waitFloor']

    if 'getEnviro' in message:
        enviro = {}
        enviro['temp1'] = '{0:0.2f} *C'.format(sensor.read_temperature())
        enviro['pres1'] = '{0:0.2f} Pa'.format(sensor.read_pressure())
        enviro['alt1']  = '{0:0.2f} m'.format(sensor.read_altitude())
        enviro['pres2'] = '{0:0.2f} Pa'.format(sensor.read_sealevel_pressure())
        enviro['humidity1'], enviro['temp2'] = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 4)

        def pubMessage(message):
            print(message)

        pubnub.publish(channel, enviro, callback=pubMessage, error=pubMessage)


        # print "Sending Environmental Stats"
        # print 'Temp = {0:0.2f} *C'.format(sensor.read_temperature())
        # print 'Pressure = {0:0.2f} Pa'.format(sensor.read_pressure())
        # print 'Altitude = {0:0.2f} m'.format(sensor.read_altitude())
        # print 'Sealevel Pressure = {0:0.2f} Pa'.format(sensor.read_sealevel_pressure())
        #


def error(message):
    print("ERROR : " + (message))


def connect(message):
    print("CONNECTED")


def reconnect(message):
    print("RECONNECTED")


def disconnect(message):
    print("DISCONNECTED")

pubnub.subscribe(channel, callback=callback, error=callback,
                 connect=connect, reconnect=reconnect, disconnect=disconnect)

# http://www.raspberrypi.org/forums/viewtopic.php?f=37&t=32826

# Initialise the PWM device using the default address
pwm = PWM(0x40, debug=False)

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
    for x in range(0,7) :
        # print str(x) + ": " + str(leds[x]['minPulseLength']) + " " + str(leds[x]['maxPulseLength']) + " " + str(leds[x]['waitFloor']) + " " + str(leds[x]['waitCeiling'])
        # Change speed of continuous servo on channel O
        pwm.setPWM(x, 0, leds[x]['minPulseLength'])
        time.sleep(random.uniform(leds[x]['waitCeiling'],leds[x]['waitFloor']))
        pwm.setPWM(x, 0, leds[x]['maxPulseLength'])
        time.sleep(random.uniform(leds[x]['waitCeiling'],leds[x]['waitFloor']))
