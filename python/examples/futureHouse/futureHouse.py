import sys
from Pubnub import Pubnub
from Adafruit_PWM_Servo_Driver import PWM
import time
import random
import Adafruit_BMP.BMP085 as BMP085
import Adafruit_DHT
import RPi.GPIO as GPIO

sensor = BMP085.BMP085()

GPIO.setmode(GPIO.BOARD)
StepPins = [26,24,22,19]

for pin in StepPins:
    print "Setup pins"
    GPIO.setup(pin,GPIO.OUT)
    GPIO.output(pin, True)


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
        print "message received for LED: " + leds[message['ledID']].name

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

    if 'openDoor' in message:
        moveDoor("open")
    elif 'closeDoor' in message:
        moveDoor("close")


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

def moveDoor(direction):

    stepCount = 8
    globalcount = 1600
    cycles = 0
    stepCounter = 0
    waitTime = 0.000001

    openSeq = range(0, stepCount)
    openSeq[0] = [1,0,0,0]
    openSeq[1] = [1,1,0,0]
    openSeq[2] = [0,1,0,0]
    openSeq[3] = [0,1,1,0]
    openSeq[4] = [0,0,1,0]
    openSeq[5] = [0,0,1,1]
    openSeq[6] = [0,0,0,1]
    openSeq[7] = [1,0,0,1]

    closeSeq = range(0, stepCount)
    closeSeq[7] = [1,0,0,0]
    closeSeq[6] = [1,1,0,0]
    closeSeq[5] = [0,1,0,0]
    closeSeq[4] = [0,1,1,0]
    closeSeq[3] = [0,0,1,0]
    closeSeq[2] = [0,0,1,1]
    closeSeq[1] = [0,0,0,1]
    closeSeq[0] = [1,0,0,1]

    # Choose a sequence to use

    if direction == "open":
        seq = openSeq
    elif direction == "close":
        seq = closeSeq
    else:
        return

    # Start main loop
    while 1==1:
        for pin in range(0, 4):
            xpin = StepPins[pin]

            pinVal = seq[stepCounter][pin]

            if pinVal!=0:
                #print " Step %i Enable %i" %(StepCounter,xpin)
                GPIO.output(xpin, True)
            else:
                GPIO.output(xpin, False)

        stepCounter += 1
        cycles +=1

        print " Stepcounter: %i" %(stepCounter)
        # If we reach the end of the sequence
        # start again
        if (stepCounter==stepCount):
            stepCounter = 0

        if (stepCounter<0):
            stepCounter = stepCount

        if (globalcount == cycles):
            sys.exit()

        # Wait before moving on
        time.sleep(waitTime)

# Initialise the PWM device using the default address
pwm = PWM(0x40, debug=False)
pwm.setPWMFreq(60)                        # Set frequency to 60 Hz
while (True):
    for x in range(0,7) :
        # print str(x) + ": " + str(leds[x]['minPulseLength']) + " " + str(leds[x]['maxPulseLength']) + " " + str(leds[x]['waitFloor']) + " " + str(leds[x]['waitCeiling'])
        # Change speed of continuous servo on channel O
        pwm.setPWM(x, 0, leds[x]['minPulseLength'])
        time.sleep(random.uniform(leds[x]['waitCeiling'],leds[x]['waitFloor']))
        pwm.setPWM(x, 0, leds[x]['maxPulseLength'])
        time.sleep(random.uniform(leds[x]['waitCeiling'],leds[x]['waitFloor']))
