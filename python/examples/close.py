#-----------------------------------
# Name: Stepper Motor
#
# Author: matt.hawkins
#
# Created: 11/07/2012
# Copyright: (c) matt.hawkins 2012
#-----------------------------------
#!/usr/bin/env python
 
# Import required libraries
import time
import sys
import RPi.GPIO as GPIO

# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BOARD)
 
# Define GPIO signals to use
# Pins 19,22,24,26
# GPIO10,GPIO25,GPIO8,GPIO7

StepPins = [26,24,22,19]
#StepPins = [24,22,26,19]
 
# Set all pins as output
for pin in StepPins:
  print "Setup pins"
  GPIO.setup(pin,GPIO.OUT)
  GPIO.output(pin, False)
 
# Define some settings
StepCounter = 0
WaitTime = 0.000001
#WaitTime = 0.001
 
# Define simple sequence
StepCount1 = 4
Seq1 = []
Seq1 = range(0, StepCount1)

Seq1[0] = [1,0,0,0]
Seq1[1] = [0,1,0,0]
Seq1[2] = [0,0,1,0]
Seq1[3] = [0,0,0,1]

#Seq1[3] = [1,0,0,0]
#Seq1[2] = [0,1,0,0]
#Seq1[1] = [0,0,1,0]
#Seq1[0] = [0,0,0,1]
 
# Define advanced sequence
# as shown in manufacturers datasheet
StepCount2 = 8
Seq2 = []
Seq2 = range(0, StepCount2)
Seq2[7] = [1,0,0,0]
Seq2[6] = [1,1,0,0]
Seq2[5] = [0,1,0,0]
Seq2[4] = [0,1,1,0]
Seq2[3] = [0,0,1,0]
Seq2[2] = [0,0,1,1]
Seq2[1] = [0,0,0,1]
Seq2[0] = [1,0,0,1]
 
# Choose a sequence to use
Seq = Seq2
StepCount = StepCount2
GlobalCount = 1600
Cycles = 0
 
# Start main loop
while 1==1:
 
  for pin in range(0, 4):
    xpin = StepPins[pin]

    pinVal = Seq[StepCounter][pin]

    if pinVal!=0:
      #print " Step %i Enable %i" %(StepCounter,xpin)
      GPIO.output(xpin, True)
    else:
      GPIO.output(xpin, False)
 
  StepCounter += 1
  Cycles +=1

  print " Stepcounter: %i" %(StepCounter) 
  # If we reach the end of the sequence
  # start again
  if (StepCounter==StepCount):
    StepCounter = 0

  if (StepCounter<0):
    StepCounter = StepCount

  if (GlobalCount == Cycles):
   sys.exit()

  # Wait before moving on
  time.sleep(WaitTime)
