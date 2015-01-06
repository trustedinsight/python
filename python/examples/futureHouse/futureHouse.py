import sys
from Pubnub import Pubnub
from Adafruit_PWM_Servo_Driver import PWM
import thread
import time
import random
import Adafruit_BMP.BMP085 as BMP085
import Adafruit_DHT
import RPi.GPIO as GPIO

# Initialize Humid / Temp

sensor = BMP085.BMP085()

# Initialize Stepper

GPIO.setmode(GPIO.BOARD)
stepPins = [26,24,22,19]
waitTime = 0.000001

for pin in stepPins:
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


channel = 'futureChannel'

# pulse lengths have a max of 4096

leds = [
    {'name': 'iceCaveLamp', 'minPulseLength': 150, 'maxPulseLength': 2600, 'waitFloor': 0.0001, 'waitCeiling': 0.005, 'proc': False},
    {'name': 'iceCaveCrystal', 'minPulseLength': 150, 'maxPulseLength': 2600, 'waitFloor': 0.0001, 'waitCeiling': 0.005, 'proc': False},
    {'name': 'fireplaceOrange', 'minPulseLength': 150, 'maxPulseLength': 2600, 'waitFloor': 0.0001, 'waitCeiling': 0.005, 'proc': False},
    {'name': 'campfire', 'minPulseLength': 150, 'maxPulseLength': 2600, 'waitFloor': 0.0001, 'waitCeiling': 0.005, 'proc': False},
    {'name': 'porchLight', 'minPulseLength': 150, 'maxPulseLength': 2600, 'waitFloor': 0.0001, 'waitCeiling': 0.005, 'proc': False},
    {'name': 'fireplaceRed', 'minPulseLength': 150, 'maxPulseLength': 2600, 'waitFloor': 0.0001, 'waitCeiling': 0.005, 'proc': False},
    {'name': 'stove', 'minPulseLength': 150, 'maxPulseLength': 2600, 'waitFloor': 0.0001, 'waitCeiling': 0.005, 'proc': False}
]

def pubMessage(message):
    print(message)

def getLEDStatus():
    pubnub.publish(channel, leds, callback=pubMessage, error=pubMessage)

def callback(message, channel):

    # LED Getters
    if 'getLEDStatus' in message:
        getLEDStatus()

    # LED Setters
    if 'ledID' in message:

        print "message received for LED: " + leds[message['ledID']]['name']

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

        getLEDStatus()


    if 'getEnviro' in message:
        enviro = {}
        enviro['temp1'] = '{0:0.2f} *C'.format(sensor.read_temperature())
        enviro['pres1'] = '{0:0.2f} Pa'.format(sensor.read_pressure())
        enviro['alt1']  = '{0:0.2f} m'.format(sensor.read_altitude())
        enviro['pres2'] = '{0:0.2f} Pa'.format(sensor.read_sealevel_pressure())
        enviro['humidity1'], enviro['temp2'] = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 4)

        pubnub.publish(channel, enviro, callback=pubMessage, error=pubMessage)

    if 'openDoor' in message:
        try:
            thread.start_new_thread( moveDoor, ("open",) )
        except:
            print "Error: unable to open door thread"

    elif 'closeDoor' in message:
        try:
            thread.start_new_thread( moveDoor, ("close",) )
        except:
            print "Error: unable to close door thread"

def error(message):
    print("ERROR : " + (message))


def connect(message):
    print("CONNECTED")
    #startCycling()


def reconnect(message):
    print("RECONNECTED")


def disconnect(message):
    print("DISCONNECTED")

def pnSubscribe():
    pubnub.subscribe(channel, callback=callback, error=callback,
                     connect=connect, reconnect=reconnect, disconnect=disconnect)

# try:
#     thread.start_new_thread( pnSubscribe, () )
# except:
#     print "Error: unable to start Subscribe thread"

pnSubscribe()

# http://www.raspberrypi.org/forums/viewtopic.php?f=37&t=32826

def moveDoor(direction):

    stepCounter = 0
    stepCount = 8

    Seq = []
    Seq = range(0, stepCount)

    if direction == "open":

        Seq[0] = [1,0,0,0]
        Seq[1] = [1,1,0,0]
        Seq[2] = [0,1,0,0]
        Seq[3] = [0,1,1,0]
        Seq[4] = [0,0,1,0]
        Seq[5] = [0,0,1,1]
        Seq[6] = [0,0,0,1]
        Seq[7] = [1,0,0,1]

    elif direction == "close":

        Seq[7] = [1,0,0,0]
        Seq[6] = [1,1,0,0]
        Seq[5] = [0,1,0,0]
        Seq[4] = [0,1,1,0]
        Seq[3] = [0,0,1,0]
        Seq[2] = [0,0,1,1]
        Seq[1] = [0,0,0,1]
        Seq[0] = [1,0,0,1]

    else:
        return

    maxSteps = 1600
    completedSteps = 0

    # Start main loop
    while completedSteps != maxSteps:

        for pin in range(0, 4):
            xpin = stepPins[pin]

            pinVal = Seq[stepCounter][pin]

            if pinVal!=0:
                #print " Step %i Enable %i" %(StepCounter,xpin)
                GPIO.output(xpin, True)
            else:
                GPIO.output(xpin, False)

        stepCounter += 1
        completedSteps +=1

        print " Stepcounter: %i" %(stepCounter)
        if (stepCounter==stepCount):
            stepCounter = 0

        if (stepCounter<0):
            stepCounter = stepCount

        time.sleep(waitTime)


# Initialise the PWM device using the default address
pwm = PWM(0x40, debug=False)
pwm.setPWMFreq(60)                        # Set frequency to 60 Hz


def cycleLEDs(x):
    leds[x]['proc'] = True
    pwm.setPWM(x, 0, leds[x]['minPulseLength'])
    time.sleep(random.uniform(leds[x]['waitCeiling'], leds[x]['waitFloor']))
    pwm.setPWM(x, 0, leds[x]['maxPulseLength'])
    time.sleep(random.uniform(leds[x]['waitCeiling'], leds[x]['waitFloor']))
    leds[x]['proc'] = False


def startCycling():
    while (True):

        for x in range(0,7) :

            if (leds[x]['proc'] == False):
                try:
                    thread.start_new_thread( cycleLEDs, (x,) )
                except:
                    print "Error: unable to start LED thread"

startCycling()
