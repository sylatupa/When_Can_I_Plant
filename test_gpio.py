#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      sylatupa
#
# Created:     03/09/2016
# Copyright:   (c) sylatupa 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import RPi.GPIO as GPIO ## Import GPIO library
import time ## Import 'time' library. Allows us to use 'sleep'

def main():

    GPIO.setmode(GPIO.BOARD) ## Use board pin numbering
    GPIO.setup(23,GPIO.OUT) ## Setup GPIO Pin 7 to OUT

    ##Define a function named Blink()


    ## Start Blink() function. Convert user input from strings to numeric data types and pass to Blink() as parameters
    iterations = raw_input("Enter total number of times to blink: ")
    speed = raw_input("Enter length of each blink(seconds): ")
    Blink(int(iterations),float(speed))


def Blink(numTimes,speed):
    for i in range(0,numTimes):## Run loop numTimes
        print "Iteration " + str(i+1)## Print current loop
        GPIO.output(23,True)## Switch on pin 7
        time.sleep(speed)## Wait
        GPIO.output(23  ,False)## Switch off pin 7
        time.sleep(speed)## Wait
    print "Done" ## When loop is complete, print "Done"
    GPIO.cleanup()

    ## Ask user for total number of blinks and length of each blink


if __name__ == '__main__':
    main()
