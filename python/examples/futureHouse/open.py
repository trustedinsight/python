import time
import sys
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
stepPins = [26,24,22,19]
waitTime = 0.000001

for pin in stepPins:
    print "Setup pins"
    GPIO.setup(pin,GPIO.OUT)
    GPIO.output(pin, False)

stepCounter = 0
stepCount = 8

Seq = []
Seq = range(0, stepCount)

Seq[0] = [1,0,0,0]
Seq[1] = [1,1,0,0]
Seq[2] = [0,1,0,0]
Seq[3] = [0,1,1,0]
Seq[4] = [0,0,1,0]
Seq[5] = [0,0,1,1]
Seq[6] = [0,0,0,1]
Seq[7] = [1,0,0,1]
 
# Choose a sequence to use

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
