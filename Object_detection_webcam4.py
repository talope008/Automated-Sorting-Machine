######## Webcam Object Detection Using Tensorflow-trained Classifier #########
#
# Author: Tristan Lopez, Christopher Nguyen
# Date: 03/18/2020
# Description: 
# This program uses a TensorFlow-trained classifier to perform object detection.
# It loads the classifier and uses it to perform object detection on a webcam feed.
# It draws boxes, scores, and labels around the objects of interest in each frame
# from the webcam.

## Some of the code is copied from Google's example at
## https://github.com/tensorflow/models/blob/master/research/object_detection/object_detection_tutorial.ipynb

## and some is copied from Dat Tran's example at
## https://github.com/datitran/object_detector_app/blob/master/object_detection_app.py

## and some is copied from Evan Juras at
## https://github.com/EdjeElectronics/TensorFlow-Object-Detection-API-Tutorial-Train-Multiple-Objects-Windows-10#2-set-up-tensorflow-directory-and-anaconda-virtual-environment


# Import packages
import os
import cv2
import numpy as np
import tensorflow as tf
import sys
import math
from scipy import interpolate as sp 

# This is needed since the notebook is stored in the object_detection folder.
sys.path.append("..")

# Import utilites
from utils import label_map_util
from utils import visualization_utils as vis_util

# Import for spline interpolation
from scipy.interpolate import interp1d

# Imports for communications
import serial
import time
from fractions import Fraction

# Open serial port uncomment
ser = serial.Serial('COM4', baudrate=115200)


# Name of the directory containing the object detection module we're using
MODEL_NAME = 'inference_graph'

# Grab path to current working directory
CWD_PATH = os.getcwd()

# Path to frozen detection graph .pb file, which contains the model that is used
# for object detection.
PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME,'frozen_inference_graph.pb')

# Path to label map file
PATH_TO_LABELS = os.path.join(CWD_PATH,'training','labelmap.pbtxt')

# Number of classes the object detector can identify
NUM_CLASSES = 5

## Load the label map.
# Label maps map indices to category names, so that when our convolution
# network predicts `5`, we know that this corresponds to `king`.
# Here we use internal utility functions, but anything that returns a
# dictionary mapping integers to appropriate string labels would be fine
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

# Load the Tensorflow model into memory.
detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')

    sess = tf.Session(graph=detection_graph)


# Define input and output tensors (i.e. data) for the object detection classifier

# Input tensor is the image
image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

# Output tensors are the detection boxes, scores, and classes
# Each box represents a part of the image where a particular object was detected
detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

# Each score represents level of confidence for each of the objects.
# The score is shown on the result image, together with the class label.
detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')

# Number of objects detected
num_detections = detection_graph.get_tensor_by_name('num_detections:0')

# Initialize webcam feed
video = cv2.VideoCapture(0)
ret = video.set(4,1280)
ret = video.set(5,720)

global position_list
position_list = []
global frame
global angle_list
angle_list = []

# Set the pickup space
pickup_R = ()
pickup_TH = ()

def distance(a):
    x1, y1 = a[0]
    x2, y2 = a[1]
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def a(event,x,y,flags,param):
    s = 9

def serial_send(x,y,bin):
    x_int= int(x*(10**5))
    print(x_int)
    y_int = int(y*(10**5))
    print(y_int)
    coords = [x_int,y_int,bin]
    #coords = [x,y,3]
    for i in range(len(coords)):
        coords[i] = (coords[i]).to_bytes(3, byteorder = 'little', signed = True)
    for i in range(len(coords)):
        ser.write(coords[i])
        print(coords[i])
        time.sleep(.25)

def get_spline(x,y):
    f = interp1d(x,y, kind='linear',axis=-1,)

def draw_circle(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN:
        overlay = frame.copy()
        cv2.circle(overlay,(x,y),3,(255,0,0),-1)
        position_list.append((x,y))
        print(x,y) 
        cv2.addWeighted(overlay, 0.7, frame, 1 - 0.7,0, frame)
        cv2.imshow('Object detector', frame)

def set_robot_center(event,x,y,flags,param):
    global overlay_axis
    global robot_center
    if event == cv2.EVENT_LBUTTONDBLCLK:
        overlay_axis = frame.copy()
        cv2.circle(overlay_axis,(x,y),5,(0,0,255),-1)
        robot_center = (x,y)
        print("Robot center: ", robot_center)

    elif event == cv2.EVENT_LBUTTONDBLCLK:
   		camera_coordinate = (x,y)
   		print("Camera Coordinate: ",camera_coordinate)

   		x_temp = camera_coordinate[0] - robot_center[0]
   		y_temp = robot_center[1] - camera_coordinate[1]
   		relative_coordinate = (x_temp, y_temp)
   		print("Coordinate relative to robot:", relative_coordinate)
   		x_temp = relative_coordinate[0] * ipp
   		y_temp = relative_coordinate[1] * ipp

   		#round down for 
   		#x_temp = int(x_temp)
   		#y_temp = int(y_temp)

   		scaled_relative_coordinate = (x_temp, y_temp)
   		print("Scaled coordinate relative to robot:", scaled_relative_coordinate)

   		r_temp = math.sqrt((x_temp**2 + y_temp**2))
   		print (r_temp)

   		th_temp = math.atan2(x_temp, y_temp)
   		print (th_temp*(180/math.pi))

   		x_hat = abs(r_offset * math.cos(th_temp))
   		y_hat = abs(r_offset * math.sin(th_temp))

   		x_offset = x_temp - x_hat
   		y_offset = y_temp - y_hat 

   		print ("New X: ", x_offset)
   		print ("New Y: ", y_offset)
   		print ((math.atan2(x_offset, y_offset)) * (180/math.pi))


def get_relative_coordinate(event,x,y,flags,param):
    r_offset = 1.72

    if event == cv2.EVENT_LBUTTONDBLCLK:
        camera_coordinate = (x,y)
        
        x_temp = camera_coordinate[0] - robot_center[0]
        y_temp = robot_center[1] - camera_coordinate[1]
        relative_coordinate = (x_temp, y_temp)
       
        x_temp = relative_coordinate[0] * ipp
        y_temp = relative_coordinate[1] * ipp
      
        scaled_relative_coordinate = (x_temp, y_temp)
        
        r_temp = math.sqrt((x_temp**2 + y_temp**2))

        th_temp = math.atan2(x_temp, y_temp)*(180/math.pi)

        angle_list.append(th_temp)
        print(angle_list)

def get_new_angle(event,x,y,flags,param):
    r_offset = 1.72

    if event == cv2.EVENT_LBUTTONDBLCLK:
        camera_coordinate = (x,y)
        
        x_temp = camera_coordinate[0] - robot_center[0]
        y_temp = robot_center[1] - camera_coordinate[1]
        relative_coordinate = (x_temp, y_temp)
       
        x_temp = relative_coordinate[0] * ipp
        y_temp = relative_coordinate[1] * ipp
      
        scaled_relative_coordinate = (x_temp, y_temp)
        
        r_temp = math.sqrt((x_temp**2 + y_temp**2))

        th_temp = math.atan2(x_temp, y_temp)*(180/math.pi)

        print("Old angle: ", th_temp, ",New angle: ", adjusted_angle(th_temp))

def calculate_relative_coordinate(x,y):
    r_offset = 1.72
    camera_coordinate = (x,y)
    # print("Camera Coordinate: ", camera_coordinate )
    
    x_temp = camera_coordinate[0] - robot_center[0]
    y_temp = robot_center[1] - camera_coordinate[1]
    relative_coordinate = (x_temp, y_temp)
    # print("Coordinate relative to robot:", relative_coordinate)    
    
    x_temp = relative_coordinate[0] * ipp
    y_temp = relative_coordinate[1] * ipp

    scaled_relative_coordinate = (x_temp, y_temp)
    # print("Scaled coordinate relative to robot:", scaled_relative_coordinate)

    r_temp = math.sqrt((x_temp**2 + y_temp**2))
    # print ("Distance from base: ", r_temp)

    th_temp = (math.atan2(x_temp, y_temp))*(180/math.pi)
    if th_temp > -5 or th_temp < -85: 
    	pass
    else:	
    	th_temp = adjusted_angle(th_temp)
	
    print ("Angle from center: ", th_temp)

    x_hat = abs(r_offset * math.cos(th_temp))
    y_hat = abs(r_offset * math.sin(th_temp))

    x_offset = x_temp - x_hat
    y_offset = y_temp - y_hat 
    scaled_offset_coordinate = (x_offset, y_offset)

    offset_angle = (math.atan2(x_offset, y_offset)) * (180/math.pi)

    # print ("New X: ", x_offset)
    # print ("New Y: ", y_offset)
    # print ("New Angle: ", offset_angle)

    return scaled_relative_coordinate, scaled_offset_coordinate, th_temp, offset_angle, r_temp

def get_bin_number(a):
    if(a == "lcd_green"):
        return 1
    elif(a == "lcd_red"):
        return 2
    elif(a == "pcb_black"):
        return 3
    elif(a == "ultrasonic"):
        return 4  
    elif(a == "led_mat"):
        return 5
    else:
        return 0                

            

cv2.namedWindow('Object detector')

print("Press 'q' to freeze the frame after setting the camera")


while(True):
    ret, frame = video.read()
    cv2.imshow('Object detector', frame)
    if cv2.waitKey(1) == ord('q'):
        break


print("Measure two points on screen")
cv2.setMouseCallback('Object detector',draw_circle)

while(True):
    cv2.imshow('Object detector', frame)
    cv2.waitKey(1)
    if (len(position_list) >= 2):
        cv2.line(frame,position_list[0],position_list[1], (0, 0, 255), 1)
        cv2.imshow('Object detector', frame)
        cv2.waitKey(1)
        length = distance(position_list)
        print('Line length: ', length) 

        break

cv2.setMouseCallback('Object detector', a)

scale = input("input the real world length of the region in inches: ")
print(scale)

ipp = (float(scale)/length)
ppi = (length/float(scale))

print("scaling factor(inches/pixel): ", ipp)
print("scaling factor(pixels/inch): ", ppi)


print("Set robot center with a double click,  press q to finalize the position")

cv2.setMouseCallback('Object detector', set_robot_center)

alpha = 1
robot_center = (0,0)

while(True):
    ret, frame = video.read()

    # cv2.line(overlay,(x1,y1),(x2,y2), (0, 0, 255), 3)
    cv2.line(frame, (robot_center[0],0), (robot_center[0], 720),(0,0,255),3)
    cv2.line(frame, (0,robot_center[1]),(1280,robot_center[1]),(0,0,255),3)

    cv2.imshow('Object detector', frame)
    if cv2.waitKey(1) == ord('q'):
        break

print("Test angles")
cv2.setMouseCallback('Object detector', get_relative_coordinate)

while(True):
    ret, frame = video.read()

    # cv2.line(overlay,(x1,y1),(x2,y2), (0, 0, 255), 3)
    cv2.line(frame, (robot_center[0],0), (robot_center[0], 720),(0,0,255),3)
    cv2.line(frame, (0,robot_center[1]),(1280,robot_center[1]),(0,0,255),3)

    cv2.imshow('Object detector', frame)

    if len(angle_list) == 12:
    	break

    l = cv2.waitKey(1)
    if l == ord('q'):
        break
    if l == ord('a'):
        print(angle_list)
    if l == ord('z'):
        angle_list.pop()
        print(angle_list)

camera_angle = np.array(angle_list)
real_angle = np.array([0,-5,-10,-20,-30,-40,-50,-60,-70,-80,-85,-90])
global adjusted_angle
adjusted_angle = sp.interp1d(camera_angle, real_angle, kind= 'linear')  
# cv2.setMouseCallback('Object detector', set_pickup_space)

# while(True):
#     ret, frame = video.read()

#     cv2.line(frame, (robot_center[0],0), (robot_center[0], 720),(0,0,255),3)
#     cv2.line(frame, (0,robot_center[1]),(1280,robot_center[1]),(0,0,255),3)

#     cv2.imshow('Object detector', frame)
#     cv2.waitKey(1)
#     if (len(pickup_space) >= 2) :


#         cv2.rectangle(frame,pickup_space[0],pickup_space[1], (0, 0, 255), 3)
        
#         cv2.line(frame, (robot_center[0],0), (robot_center[0], 720),(0,0,255),3)
#         cv2.line(frame, (0,robot_center[1]),(1280,robot_center[1]),(0,0,255),3)

#         cv2.imshow('Object detector', frame)
#         length = distance(pickup_space)

#         break



print('Testing')
cv2.setMouseCallback('Object detector', get_new_angle)
while(True):
    ret, frame = video.read()

    # cv2.line(overlay,(x1,y1),(x2,y2), (0, 0, 255), 3)
    cv2.line(frame, (robot_center[0],0), (robot_center[0], 720),(0,0,255),3)
    cv2.line(frame, (0,robot_center[1]),(1280,robot_center[1]),(0,0,255),3)

    cv2.imshow('Object detector', frame)

    l = cv2.waitKey(1)
    if l == ord('q'):
    	break

th_min, th_max = -80,-20 
pickup_space = (th_min, th_max)

image_width, image_height = frame.shape[:2]


# Wait for Pi to send a ready check
print ("Waiting for Pi")

ser.read(1)

print ("Received")

while(True):

    flag = True
    m = 0
    while (flag): 
        # Acquire frame and expand frame dimensions to have shape: [1, None, None, 3]
    # i.e. a single-column array, where each item in the column has the pixel RGB value
        ret, frame = video.read()
        frame_expanded = np.expand_dims(frame, axis=0)


        # Perform the actual detection by running the model with the image as input
        # global boxes, scores, classes, num
        (boxes, scores, classes, num) = sess.run(
            [detection_boxes, detection_scores, detection_classes, num_detections],
            feed_dict={image_tensor: frame_expanded})

        # Draw the results of the detection (aka 'visulaize the results')
        vis_util.visualize_boxes_and_labels_on_image_array(
            frame,
            np.squeeze(boxes),
            np.squeeze(classes).astype(np.int32),
            np.squeeze(scores),
            category_index,
            use_normalized_coordinates=True,
            line_thickness=8,
            min_score_thresh=0.80)

        # Overlay center
        cv2.line(frame, (robot_center[0],0), (robot_center[0], 720),(0,0,255),3)
        cv2.line(frame, (0,robot_center[1]),(1280,robot_center[1]),(0,0,255),3)

        # All the results have been drawn on the frame, so it's time to display it.
        cv2.imshow('Object detector', frame)
        cv2.waitKey(1)

        m += 1
        # if m less than threshold don't
        if (m > 55):
	        # Check if object is within the ROI
	        i = 0
	        for i in range(0,5):
	            print("checking ROI")
	            pos = boxes[0][i]
	            (xmin, xmax, ymin, ymax) = (pos[1]*image_width, pos[3]*image_width, pos[0]*image_height, pos[2]*image_height)
	            (x,y) = (((xmax + xmin)/2) , ((ymax + ymin)/2))
	            scaled_relative_coordinate, scaled_offset_coordinate, th_temp, offset_angle, dist = calculate_relative_coordinate(x,y)
	            # ROI bounds if inside min and max
	            if dist > 3 and th_temp > th_min and th_temp < th_max :
	                
	                print ("Class: ", category_index[classes[0][i]]['name'], "Position: ", (scaled_relative_coordinate), "Angle: ", th_temp)
	                time.sleep(5)

	                x_temp, y_temp = scaled_relative_coordinate    
	                serial_send(x_temp,y_temp,get_bin_number(category_index[classes[0][i]]['name']))
	                flag = False
	                break
	            i += 1   


    # Press 'q' to quit
    if cv2.waitKey(1) == ord('q'):
        break 


# Clean up
video.release()
cv2.destroyAllWindows()

