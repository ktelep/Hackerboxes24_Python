import numpy as np
import serial
import cv2
import struct
from time import sleep

# Setup our Serial Port
serial_port = "COM8"  # Serial port the Arduino is attached to
serial_speed = 9600   # Speed we're talking to it

# These are used for facial detection
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

# Some defaults  
tilt_chan = 0   # This is the channel 'Tilt' is on when talking to Arduino
pan_chan = 1    # This is the channel 'Pan' is on when talking to Arduino
cur_pan = 90    # Sane defaults for the current pan
cur_tilt = 70   # Sane defaults for the current tile
center_tolerance = 20   # How tolerant are we of the center, we're using a 40x40 box here
camera_fov_x = 42   # Cameras view in x degrees
camera_fov_y = 50   # Cameras view in y degrees


def setServo(pan, tilt):

   # Some sanity checks to make sure we don't go over what our servo can do
   if pan < 0: pan = 0
   if pan > 180: pan = 180
   if tilt < 0: tilt = 0
   if tilt > 180: tilt = 180

   # We're reading these values as bytes on the arduino, why make it convert
   # strings to ints over there when we can just sent them natively from here?
   # So we're going to pack them and send as bytes

   ser.write(struct.pack('>BBBB',pan_chan,pan,tilt_chan,tilt))

def moveServo(direction, degrees):
   # Calculate our new servo position and send it to setServo to move it

   print "Direction: %s  Degrees: %d" % (direction, degrees)
   global cur_pan
   global cur_tilt
   if direction=="LEFT":
       cur_pan = cur_pan + degrees
   if direction=="RIGHT":
       cur_pan = cur_pan - degrees
   if direction=="UP":
       cur_tilt = cur_tilt - degrees
   if direction=="DOWN":
       cur_tilt = cur_tilt + degrees

   setServo(cur_pan,cur_tilt)

def exerciseServo():
    # Exercise the servo then set it to the middle
    setServo(0,90)
    sleep(1)
    setServo(180,0)
    sleep(1)
    setServo(180,180)
    sleep(1)
    setServo(0,180)
    sleep(1)
    setServo(90,75)


# Open up our serial port to talk to the Arduino
ser = serial.Serial(serial_port, serial_speed)

# Capture video from the default video camera
cap = cv2.VideoCapture(0)

if cap.isOpened():
    # Show some quick debug info
    x_res = cap.get(3)
    y_res = cap.get(4)
    cam_midpoint_x = x_res/2
    cam_midpoint_y = y_res/2

    print "Capture Setup"
    print "-----------------------"
    print " X-Resolution: %d" % (x_res,)
    print " Y-Resolution: %d" % (y_res,)
    print " Cam Midpoint X: %d Y: %d" % (cam_midpoint_x, cam_midpoint_y)

# Test out our servos to make sure everything is working
exerciseServo()

while(True):
    # Capture frame-by-frame
    ret, img = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Face Detection from https://docs.opencv.org/3.3.0/d7/d8b/tutorial_py_face_detection.html
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:
        # Draw a rectangle around faces and eyes
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]

        # Detection returns the upper left of the bounding box of the face
        # However we want the middle of the face, thankfully we get the width and height
        face_midpoint_x = x+(w/2)
        face_midpoint_y = y+(h/2)

        # We're going to calculate where the camera needs to point based on a couple things
        # and then move it
        if face_midpoint_y < (cam_midpoint_y - center_tolerance):
            degrees_per_move = int((cam_midpoint_y - face_midpoint_y) / (camera_fov_y/2))
            moveServo("UP", degrees_per_move)
        elif face_midpoint_y > (cam_midpoint_y + center_tolerance):
            degrees_per_move = int((face_midpoint_y - cam_midpoint_y) / (camera_fov_y/2))
            moveServo("DOWN", degrees_per_move)
        if face_midpoint_x > (cam_midpoint_x + center_tolerance):
            degrees_per_move = int((face_midpoint_x - cam_midpoint_x) / (camera_fov_x/2))
            moveServo("RIGHT", degrees_per_move)
        elif face_midpoint_x <  (cam_midpoint_x - center_tolerance):
            degrees_per_move = int((cam_midpoint_x - face_midpoint_x) / (camera_fov_x/2))
            moveServo("LEFT", degrees_per_move)

    # Display the resulting frame
    cv2.imshow('frame',img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
