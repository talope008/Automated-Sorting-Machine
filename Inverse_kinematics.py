import pigpio
import math
from time import sleep
from math import pi, sqrt


#'''
#lab 4 - and some fo rlab 7
#'''
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

Color_List = {
    'blue' : {'color': 'blue', 'x_location': 5, 'y_location': 4},
    'red': {'color': 'red', 'x_location': 0, 'y_location': 0},
    'green': {'color': 'green', 'x_location': 1, 'y_location': 1}

}

def object_location_PWM(x,y):
    theta = math.atan2(x,y)
    #implement rads to degrees
    print "theta of ", x, " and ", y, " = ", theta


    angle = theta * (180 / math.pi)
    print "angle of theta = " , angle


    PWM_servo1 = (angle / -90) + 1.5
    PWM_servo1 = int(PWM_servo1 * 1000)
    PWM_servo1 = int(PWM_servo1/5) *5

    return PWM_servo1 # move to this point

def lowering_angles_PWM(x):
    a = 4.75 #fixed values of arms to elbow
    b = 7 #elbow to gripper
    height = -7 # axis invertered so more negative = higher up

    c = sqrt(x**2 + height**2) #calculate to move servo at the bottom
    print "c: ", c

    A = math.degrees(math.acos((a**2 - b**2 - c**2) / (-2 * b * c)))
    B = math.degrees(math.acos((b**2 - a**2 - c**2) / (-2 * a * c)))
    C = 180 - A - B
    B = 90 - B
    print "C: ", C
    print "B: ", B

    lowering_angle_B = B #main servo to move elbow
    print "Main servo to move elbow: ", B
    lowering_angle_C = C #secondary servo to move
    print "Main servo to move elbow: ", C
    print "Lower angles"
    PWM_servo2  = 0
    #sleep(10)
    lowering_angle_C -= 110
    PWM_servo2 = (lowering_angle_B / 90) + 1.5
    PWM_servo2 = int(PWM_servo2 * 1000)
    PWM_servo2 = int(PWM_servo2/5) * 5
    
    print "PWM servo 2 : ", PWM_servo2
    #sleep(10)
    return PWM_servo2

def bin_location_PWM(bin):
    x_bin = Color_List.get(bin)["x_location"]
    y_bin = Color_List.get(bin)["y_location"]
    #---------------------------------------------------------
    theta = math.atan2(x_bin,y_bin)
    #implement rads to degrees
    print "theta of ", x_bin, " and ", y_bin, " = ", theta


    angle = theta * (180 / math.pi)
    print "angle of theta = " , angle


    PWM_servo1 = (angle / -90) + 1.5
    bin_locationPWM = int(PWM_servo1 * 1000)

    print "int PWM = ", bin_locationPWM
    bin_locationPWM = int(bin_locationPWM/5) * 5
    print "mod 5 PWM: = ", bin_locationPWM

    return bin_locationPWM

def grip():

    i =500

    while i != 2300:
        pi.set_servo_pulsewidth(25,i)
        sleep(0.001)
        i += 5
        print('gripping',i)

    return

def release():

    i = 2400

    while i != 710:
        pi.set_servo_pulsewidth(25,i)
        sleep(0.001)
        i += -5
        print('release',i)

    return

def lower(x):
    
    global curr_PWM_servo2
    
    Next_PWM_servo2 = lowering_angles_PWM(x)
    print(Next_PWM_servo2)
    
    if(Next_PWM_servo2 < curr_PWM_servo2):
        while curr_PWM_servo2 != Next_PWM_servo2:
            pi.set_servo_pulsewidth(23,curr_PWM_servo2)
            sleep(0.001)
            curr_PWM_servo2 += -2.5
            print "lowering servo2 1", curr_PWM_servo2

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
            print "Raising servo2 1", curr_PWM_servo2
            

    elif(initial_PWM_servo2 > curr_PWM_servo2):
        while curr_PWM_servo2 != initial_PWM_servo2:
            pi.set_servo_pulsewidth(23,curr_PWM_servo2)
            sleep(0.002)
            curr_PWM_servo2 += 5
            print("Raising servo2 2", curr_PWM_servo2)
            

    else:
        curr_PWM_servo2  = PWM_servo2
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
    
    
    
def initialize_servos():
    global initial_PWM_servo1 #zero pos
    global initial_PWM_servo2 
    global initial_PWM_servo3 
    global initial_PWM_servo4
    initial_PWM_servo1 = 1500 #zero pos
    initial_PWM_servo2 = 900
    initial_PWM_servo3 = 500
    initial_PWM_servo4 = 1500
    
    global curr_PWM_servo1  #zero pos
    global curr_PWM_servo2 
    global curr_PWM_servo3 
    curr_PWM_servo1 = 1500 #zero pos
    curr_PWM_servo2 = 900
    curr_PWM_servo3 = 500

    sleep(1)
    pi.set_servo_pulsewidth(18,initial_PWM_servo1)
    print "initialize base servo"
    sleep(1) #goes to zero position
    pi.set_servo_pulsewidth(23,initial_PWM_servo2) #goes to zero position
    print "initialize lowering servo"
    pi.set_servo_pulsewidth(24,initial_PWM_servo4) #goes to zero position
    print "initialize elbow servo"
    pi.set_servo_pulsewidth(25,initial_PWM_servo3)
    sleep(1)
    print "initalize gripper"

def movetopoint(x,y,bin):
    
    Next_bin_location_PWM = bin_location_PWM(bin)
    
    movebase(x,y)
    sleep(1)
    
    lower(x)
    sleep(1)
    
    grip()
    sleep(1)
    rise()
    
    sleep(1)
    
    back2origin()
    sleep(1)
    lower(x)
    sleep(1)
    release()
    rise()
initialize_servos()
movetopoint(-7.693485365609261,6.3226282772328135,'blue')
sleep(1)
movetopoint(-9.251,0,'blue')
