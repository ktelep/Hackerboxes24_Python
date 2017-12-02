import numpy as np
import serial
import cv2
import struct
from time import sleep

# Setup our Serial Port
serial_port = "COM5"  # Serial port the Arduino is attached to
serial_speed = 9600   # Speed we're talking to it
ser = serial.Serial(serial_port, serial_speed)

# These are used for facial detection
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

# Some defaults for starting our servo
tilt_chan = 0
pan_chan = 1
cur_pan = 90;
cur_tilt = 90;


def setServo(pan, tilt):

   # Some sanity checks
   if pan < 0: pan = 0
   if pan > 180: pan = 180
   if tilt < 0: tilt = 0
   if tilt > 180: tilt = 180

   # We're reading these values as bytes on the arduino, why make it convert
   # strings to ints over there when we can just sent them natively from here?
   # So we're going to pack them and send as bytes
   ser.write(struct.pack('>BBBB',pan_chan,pan,tilt_chan,tilt))

def moveServo(direction, degrees):
   global cur_pan
   global cur_tilt
   if direction=="LEFT":
       cur_pan = cur_pan - degrees
   if direction=="RIGHT":
       cur_pan = cur_pan + degrees
   if direction=="UP":
       cur_tilt = cur_tilt + degrees
   if direction=="DOWN":
       cur_tilt = cur_tilt - degrees

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
    setServo(90,90)


# Capture video from the default video camera
cap = cv2.VideoCapture(0)

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

        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

        # Display the resulting frame
        cv2.imshow('frame',img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # move the camera as appropriate
        if y < 100:
            moveServo("UP", 2)
        elif y > 120:
            moveServo("DOWN", 2)
        if x > 250:
            moveServo("RIGHT", 2)
        elif x < 180:
            moveServo("LEFT", 2)

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
