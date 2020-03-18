######## Ultrasound Detection with Motor COntrol #########
#
# Author: Jake Ongkingco
# Date: 3/18/2020
# Description: 
# This program detects measures distance of an object and controls the dc motor
# depending on how far the object is

## Some of the code is copied from a code example at
## https://www.electronicshub.org/controlling-a-dc-motor-with-raspberry-pi/

## and also from: http://www.raspberrypirobotics.com
## /connecting-a-ultrasonic-sensor-hc-sr04-distance-sensor-to-a-raspberry-pi/

#Libraries
import RPi.GPIO as GPIO
import time
 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
flag = 1
#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24
Motor1A = 40
Motor1B = 38
Motor1E = 36

#set GPIO direction (IN / OUT)
GPIO.setup(Motor1A,GPIO.OUT)  # All pins as Outputs
GPIO.setup(Motor1B,GPIO.OUT)
GPIO.setup(Motor1E,GPIO.OUT)

GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
 
def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
    GPIO.output(Motor1E,GPIO.HIGH)
    while flag == 1:
        if(distance < 6):
            GPIO.output(Motor1A,GPIO.HIGH)
            GPIO.output(Motor1B,GPIO.LOW)
            GPIO.output(Motor1E,GPIO.HIGH)
            return distance
        else
            return distance
    return distance
 
if __name__ == '__main__':
    try:
        while True:
            dist = distance()
            print ("Measured Distance = %.1f cm" % dist)
            time.sleep(1)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
