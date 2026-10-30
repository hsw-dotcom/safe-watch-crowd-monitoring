######## Webcam Object Detection Using Tensorflow-trained Classifier #########
#
# Author: Evan Juras
# Date: 11/11/22
# Description: 
# This program uses a TensorFlow Lite object detection model to perform object 
# detection on an image or a folder full of images. It draws boxes and scores 
# around the objects of interest in each image.
#
# This code is based off the TensorFlow Lite image classification example at:
# https://github.com/tensorflow/tensorflow/blob/master/tensorflow/lite/examples/python/label_image.py
#
# I added my own method of drawing boxes and labels using OpenCV.

# Import packages
import os
import argparse
import cv2
import numpy as np
import sys
import glob
import importlib.util
import matplotlib.pyplot as plt
from tflite_runtime.interpreter import Interpreter

width, height = 640, 640 # image width, height
min_conf_threshold = 0.2 # confidecne level
input_mean = 127.5
input_std = 127.5
image_path = '/home/pi/project/image/before.jpg'
output_path = '/var/www/html/tensorflow/'


def detect():
    base_path = 'models/'
    people_model = base_path + 'people_detect.tflite'
    people_label = base_path + 'people_label.txt'
    obstacle_model = base_path + 'obstacle_detect.tflite'
    obstacle_label = base_path + 'obstacle_label.txt'

    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    imH, imW, _ = image.shape
    image_resized = cv2.resize(image_rgb, (width, height))
    input_data = np.expand_dims(image_resized, axis=0)

    people_boxes, people_classes, people_scores, people_labels = load_model(people_model, people_label, input_data)
#    obstacle_boxes, obstacle_classes, obstacle_scores, obstacle_labels = load_model(obstacle_model, obstacle_label)

    obstacle_classes = []

    people_num = 0
    for i in range(len(people_scores)):
        if people_scores[i] >= min_conf_threshold and people_classes[i] == 0:
            people_num += 1

    print("감지된 인원 수 :", people_num)

    draw_boxes(people_boxes, people_classes, people_scores, people_labels, (0, 255, 0), image)
    #    draw_boxes(obstacle_boxes, obstacle_classes, obstacle_scores, obstacle_labels, (255, 0, 0))
    cv2.imwrite(output_path + 'after.jpg', image)

    return people_num, obstacle_classes


def load_model(model_path, label_path, input_data):
    input_data_l = input_data
    # Load the label map
    with open(label_path, 'r') as f:
        labels = [line.strip() for line in f.readlines()]

    interpreter = Interpreter(model_path=model_path)
    interpreter.allocate_tensors()

    # Get model details
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    floating_model = (input_details[0]['dtype'] == np.float32)

    # Normalize pixel values if using a floating model (i.e. if model is non-quantized)
    if floating_model:
        input_data_l = (np.float32(input_data_l) - input_mean) / input_std

    outname = output_details[0]['name']
    if ('StatefulPartitionedCall' in outname):  # This is a TF2 model
        boxes_idx, classes_idx, scores_idx = 1, 3, 0
    else:  # This is a TF1 model
        boxes_idx, classes_idx, scores_idx = 0, 1, 2

    # Perform the actual detection by running the model with the image as input
    interpreter.set_tensor(input_details[0]['index'], input_data_l)
    interpreter.invoke()

    # Retrieve detection results
    boxes = interpreter.get_tensor(output_details[boxes_idx]['index'])[0]  # Bounding box coordinates of detected objects
    classes = interpreter.get_tensor(output_details[classes_idx]['index'])[0]  # Class index of detected objects
    scores = interpreter.get_tensor(output_details[scores_idx]['index'])[0]  # Confidence of detected objects
    return boxes, classes, scores, labels


def draw_boxes(boxes, classes, scores, labels, box_color, image):
    imW, imH = 1920, 1080
    # Loop over all detections and draw detection box if confidence is above minimum threshold
    for i in range(len(scores)):
        if ((scores[i] > min_conf_threshold) and (scores[i] <= 1.0) and classes[i] == 0):
            # Get bounding box coordinates and draw box
            # Interpreter can return coordinates that are outside of image dimensions, need to force them to be within image using max() and min()
            ymin = int(max(1,(boxes[i][0] * imH)))
            xmin = int(max(1,(boxes[i][1] * imW)))
            ymax = int(min(imH,(boxes[i][2] * imH)))
            xmax = int(min(imW,(boxes[i][3] * imW)))

            cv2.rectangle(image, (xmin,ymin), (xmax,ymax), box_color, 2) # hbox

            # Draw label
            object_name = labels[int(classes[i])] # Look up object name from "labels" array using class index
            label = '%s: %d%%' % (object_name, int(scores[i]*100)) # Example: 'person: 72%'
            labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2) # Get font size
            label_ymin = max(ymin, labelSize[1] + 10) # Make sure not to draw label too close to top of window
#            cv2.rectangle(image, (xmin, label_ymin-labelSize[1]-10), (xmin+labelSize[0], label_ymin+baseLine-10), (255, 255, 255), cv2.FILLED)  # Draw white box to put label text in
#            cv2.putText(image, label, (xmin, label_ymin-7), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2) # Draw label text

