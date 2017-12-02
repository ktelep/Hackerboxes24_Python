
Description
-----------------
This project is the implementation for Hackerboxes #24 using OpenCV and Python instead of Processing.   I had too much pain trying to get all the right versions of OpenCV, Java, Processing, etc. to work and realized that it was only a few python modules that cleanly installed on my Windows System.


Installation 
-------------------------
Use the installation instructions found here for Python and OpenCV:

http://opencv-python-tutroals.readthedocs.io/en/latest/index.html

I recommend installing Python 2.7 first, then just using pip to install numpy and matplotlib.

You also will need to install pySerial, also via pip.

Configuration
--------------------------
0.  Connect everything via USB to your PC (Camera and Arduino)
1.  Upload the ino file to your Arduino, note the COM port
2.  Set the serial port and speed in the top of the cap_test.py file
3.  Start the python script

The Servo should exercise itself, the expectation is that 90 degrees is straight up and down, you may need to move the upper U shaped bar on the servo spindle to compensate for this, or you can muck with the code to fix.

After exercising you should see video on screen with a box around the face that is being detected.  It should follow you pretty well.  


