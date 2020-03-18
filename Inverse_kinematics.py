######## Inverse Kinematics for 4 dof Manipulator #########
#
# Author: Anthony Castro
# Date: 2/16/2020
# Description: 
# This program uses PIGPIO Library to move 4 sevos on a 4 dof Robotic Manipulator.
# Using PWM formula to get the angles we can send PWM values using the PIGPIO function


import pigpio
import math
from time import sleep
from math import pi, sqrt
import serial
import sys
ser = serial.Serial('/dev/ttyS0', baudrate=115200, timeout=None) #No time out value, read until requested number of bytes are recieved


pi = pigpio.pi()
bin_locationPWM = 0
curr_angle = 0
curr_PWM  = 0

#print "initial positions"
initial_PWM_servo1 = 1500 #zero pos
initial_PWM_servo2 = 900
initial_PWM_servo3 = 500
initial_PWM_servo4 = 1500

curr_PWM_servo1 = 1500 #zero pos
curr_PWM_servo2 = 900
curr_PWM_servo3 = 500


#1. lcd_green, 2.motor 3. lcd_red 4. pcb_black 5.ultrasonic 6.lcd_mat

def object_location_PWM(x,y):
    theta = math.atan2(x,y)
    #implement rads to degrees
#     print ("theta of ", x, " and ", y, " = ", theta)


    angle = theta * (180 / math.pi)
#     print "angle of theta = " , angle


    PWM_servo1 = (angle / -90) + 1.5
    PWM_servo1 = int(PWM_servo1 * 1000)
    PWM_servo1 = int(PWM_servo1/5) *5

    return PWM_servo1 # move to this point

def lowering_angles_PWM(x):
    
    PWM_servo2 = 2100
    
#     print "PWM servo 2 : ", PWM_servo2
    #sleep(10)
    return PWM_servo2


def grip():

    i =500

    while i != 2450:
        pi.set_servo_pulsewidth(25,i)
        sleep(0.001)
        i += 5
        print('gripping',i)

    return

def release():

    i = 2450

    while i != 710:
        pi.set_servo_pulsewidth(25,i)
        sleep(0.001)
        i += -5
        print('release',i)

    return

def lower(temp):
    
    global curr_PWM_servo2
    
    Next_PWM_servo2 = temp
    print(Next_PWM_servo2)
    
    if(Next_PWM_servo2 < curr_PWM_servo2):
        while curr_PWM_servo2 != Next_PWM_servo2:
            pi.set_servo_pulsewidth(23,curr_PWM_servo2)
            sleep(0.001)
            curr_PWM_servo2 += -2.5
#             print "lowering servo2 1", curr_PWM_servo2

    elif(Next_PWM_servo2 > curr_PWM_servo2):
        while curr_PWM_servo2 != Next_PWM_servo2:
            pi.set_servo_pulsewidth(23,curr_PWM_servo2)
            sleep(0.001)
            curr_PWM_servo2 += 2.5
            print("lowering servo2 2", curr_PWM_servo2)

    else:
        curr_PWM_servo2  = Next_PWM_servo2
        pi.set_servo_pulsewidth(23,curr_PWM_servo2)
        
def rise():

    global initial_PWM_servo2
    global curr_PWM_servo2
    
    if(initial_PWM_servo2 < curr_PWM_servo2):
        while curr_PWM_servo2 != initial_PWM_servo2:
            pi.set_servo_pulsewidth(23,curr_PWM_servo2)
            sleep(0.002)
            curr_PWM_servo2 += -5
#             print "Raising servo2 1", curr_PWM_servo2
            

    elif(initial_PWM_servo2 > curr_PWM_servo2):
        while curr_PWM_servo2 != initial_PWM_servo2:
            pi.set_servo_pulsewidth(23,curr_PWM_servo2)
            sleep(0.002)
            curr_PWM_servo2 += 5
            print("Raising servo2 2", curr_PWM_servo2)
            

    else:
        curr_PWM_servo2  = initial_PWM_servo2
        pi.set_servo_pulsewidth(23,curr_PWM_servo2)
        
def movebase(x,y):

    Next_PWM_servo1 = object_location_PWM(x,y)
    global curr_PWM_servo1
    
    if(Next_PWM_servo1 > curr_PWM_servo1):
        while curr_PWM_servo1 != Next_PWM_servo1:
            pi.set_servo_pulsewidth(18,curr_PWM_servo1)
            sleep(0.001)
            curr_PWM_servo1 += 2.5
            print("rotating to servo1 position 1", curr_PWM_servo1)

    elif(Next_PWM_servo1 < curr_PWM_servo1):
        while curr_PWM_servo1 != Next_PWM_servo1:
            pi.set_servo_pulsewidth(18,curr_PWM_servo1)
            sleep(0.001)
            curr_PWM_servo1 += -2.5
            print("rotating to servo1 position 2", curr_PWM_servo1)

    else:
        curr_PWM_servo1  = Next_PWM_servo1
        pi.set_servo_pulsewidth(18,curr_PWM_servo1)

def movebasetobin(bin_num):
    
    Next_bin_location_PWM = bin_location_PWM(bin_num)
   
    global curr_PWM_servo1
    
    if(Next_bin_location_PWM > curr_PWM_servo1):
        while curr_PWM_servo1 != Next_bin_location_PWM:
            pi.set_servo_pulsewidth(18,curr_PWM_servo1)
            sleep(0.001)
            curr_PWM_servo1 += 2.5
            print("rotating to bin position 1", curr_PWM_servo1)

    elif(Next_bin_location_PWM < curr_PWM_servo1):
        while curr_PWM_servo1 != Next_bin_location_PWM:
            pi.set_servo_pulsewidth(18,curr_PWM_servo1)
            sleep(0.001)
            curr_PWM_servo1 += -2.5
            print("rotating to bin position 2", curr_PWM_servo1)

    else:
        curr_PWM_servo1  = Next_bin_location_PWM
        pi.set_servo_pulsewidth(18,curr_PWM_servo1)

def back2origin():
    
    global initial_PWM_servo1 #zero pos
    global initial_PWM_servo2 
    global initial_PWM_servo3 
    global initial_PWM_servo4
    global curr_PWM_servo1  #zero pos
    global curr_PWM_servo2 
    global curr_PWM_servo3
    
    
    if(initial_PWM_servo1 > curr_PWM_servo1):
        while curr_PWM_servo1 != initial_PWM_servo1:
            pi.set_servo_pulsewidth(18,curr_PWM_servo1)
            sleep(0.00125)
            curr_PWM_servo1 += 2.5
            print("rotating to servo1 position 1", curr_PWM_servo1)

    elif(initial_PWM_servo1 < curr_PWM_servo1):
        while curr_PWM_servo1 != initial_PWM_servo1:
            pi.set_servo_pulsewidth(18,curr_PWM_servo1)
            sleep(0.00125)
            curr_PWM_servo1 += -2.5
            print("rotating to servo1 position 2", curr_PWM_servo1)

    else:
        curr_PWM_servo1  = initial_PWM_servo1
        pi.set_servo_pulsewidth(18,curr_PWM_servo1)
    
def bin_location_PWM(bin_num):
    global bin_locationPWM
    if bin_num == 1: 
        bin_locationPWM = 1350
    elif bin_num == 2:
        bin_locationPWM = 1350
    elif bin_num == 3:
        bin_locationPWM = 925
    elif bin_num == 4:
        bin_locationPWM = 925
    elif bin_num == 5:
        bin_locationPWM = 580
    elif bin_num == 6:
        bin_locationPWM = 580   
    '''
    #---------------------------------------------------------
    theta = math.atan2(x_bin,y_bin)
    #implement rads to degrees
#     print "theta of ", x_bin, " and ", y_bin, " = ", theta


    angle = theta * (180 / math.pi)
#     print "angle of theta = " , angle


    PWM_servo1 = (angle / -90) + 1.5
    bin_locationPWM = int(PWM_servo1 * 1000)

#     print "int PWM = ", bin_locationPWM
    bin_locationPWM = int(bin_locationPWM/5) * 5
#     print "mod 5 PWM: = ", bin_locationPWM
    sleep(1)
    '''
    return bin_locationPWM    
    
def initialize_servos():
    
    global initial_PWM_servo1 #zero pos
    global initial_PWM_servo2 
    global initial_PWM_servo3 
    global initial_PWM_servo4
    initial_PWM_servo1 = 1500 #zero pos of base
    initial_PWM_servo2 = 700  # elbow 900
    initial_PWM_servo3 = 500  #grip
    initial_PWM_servo4 = 1500 # 1500 2nd elbow close to 500 extends
    
    global curr_PWM_servo1  #zero pos
    global curr_PWM_servo2 
    global curr_PWM_servo3 
    curr_PWM_servo1 = 1500 #zero pos
    curr_PWM_servo2 = 900
    curr_PWM_servo3 = 500

    sleep(1)
    pi.set_servo_pulsewidth(18,initial_PWM_servo1)
#     print "initialize base servo"
    sleep(1) #goes to zero position
    pi.set_servo_pulsewidth(23,initial_PWM_servo2) #goes to zero position
#     print "initialize lowering servo"
    pi.set_servo_pulsewidth(24,initial_PWM_servo4) #goes to zero position
#     print "initialize elbow servo"
    pi.set_servo_pulsewidth(25,initial_PWM_servo3)
    sleep(1)
#     print "initalize gripper"

def movetopoint(x,y,bin_num):
    
    movebase(x,y)
    sleep(1)
    
    lower(1800)
    sleep(1)
    
    grip()
    sleep(1)
    
    rise()
    sleep(1)
    
    movebasetobin(bin_num)
    sleep(1)
    
    
    lower(1200)
    sleep(1)
    
    release()
    sleep(1)
    
    rise()
    sleep(1)
    
    back2origin()
    sleep(1)
    
while (True):    
    initialize_servos()
    #Begin comms
    coords = [0,0,0]
    ready = (1).to_bytes(1, byteorder = 'little', signed = False)
    ser.write(ready)
    for i in range(len(coords)):
          coords[i] = ser.read(3)

    print(coords)

    for i in range(len(coords)):
          coords[i] = int.from_bytes(coords[i], byteorder = 'little', signed=True)

    x = coords[0]/(10**5)
    y = coords[1]/(10**5)
    b = coords[2]
    print(b)
    print(x)
    print(y)
    #End comms
    movetopoint(x,y,b)
    sleep(1)
    #movetopoint(-10.9565217391,4.304347826,'blue')
    #1. lcd_green, 2.motor 3. lcd_red 4. pcb_black 5.ultrasonic 6.lcd_mat
