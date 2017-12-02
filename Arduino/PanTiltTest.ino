#include <Servo.h>

Servo servoTilt, servoPan;

char serialChar=0;

char tiltChannel=0, panChannel=1;

void setup()
{
  servoTilt.attach(2);  //The Tilt servo is attached to pin 2
  servoPan.attach(3);   //The Pan servo is attached to pin 3
  Serial.begin(9600);
}

void loop()
{
  while(Serial.available() <=0); 
  serialChar = Serial.read();     //Copy the character from the serial port to the variable
  if(serialChar == tiltChannel){  //Check to see if the character is the servo ID for the tilt servo
    while(Serial.available() <=0);  //Wait for the second command byte from the serial port.
    servoTilt.write(Serial.read());  //Set the tilt servo position to the value of the second command byte received on the serial port
  }
  else if(serialChar == panChannel){ //Check to see if the initial serial character was the servo ID for the pan servo.
    while(Serial.available() <= 0);  //Wait for the second command byte from the serial port.
    servoPan.write(Serial.read());   //Set the pan servo position to the value of the second command byte received from the serial port.
  }
  //If the character is not the pan or tilt servo ID, it is ignored.
}
