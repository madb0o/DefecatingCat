/*
Airsoft Turrent System Control

This code receives serial commands from the controlling system 
and can move the X/Y coordinates of the pan/tilt system to target position
and can fire the weapon using an NPN transistor to initiate 500MS bursts. 

Author: Adam Meyers - madboo@d0ubletap.net

Inputs: CommandBYte (Fire or Move)
Optional Inputs: X,Y (Position coordinates)


Outputs: None

*/

#include <Servo.h>


Servo myservoX, myservoY; // Servo variables definition
int incomingByteCommand,incomingByteX,incomingByteY = 0;  // Initiate Command, X, and Y variables to 0
int ledPin = 13;  // Internal Led PIN
int Weapon = 5;  // Airsoft Gun transistor control

void setup() 
{ 
  myservoX.attach(6);  // X axis servo for weapon movement
  myservoY.attach(9);  // Y axis servo for weapon movement
  myservoX.write(90);  // Initialize X axis servo to center
  myservoY.write(90);  // Initialize Y axis servo to center
  pinMode(Weapon, OUTPUT);  // Initialize the Airsoft gun Pin
  Serial.begin(9600);  // Initialize Serial Interface
  while (!Serial) {
    ;                  // Wait for Serial
  }
  Serial.println("Arduino Online - Awaiting Target Coordinates");
  digitalWrite(ledPin,HIGH); //Activate the led
  
}

void loop()
{
  if (Serial.available() > 2) {
    incomingByteCommand = Serial.read(); // Command Byte
    switch(incomingByteCommand) {  // Switch statement for command 
      case 255:  // Case 0xFF initiate movement
        incomingByteX = Serial.read();  // Receive the X coordinate position 
        incomingByteY = Serial.read();  // Receive the Y coordinate position
        myservoX.write(incomingByteX);  // Position X axis
        myservoY.write(incomingByteY);  // Position Y axis
        break;  
      case 254:  // Case 0xFE Fire the airsoft gun
        digitalWrite(Weapon, HIGH);  // High voltage initiates NPN transistor saturation
        delay(500);  // 500ms delay for firing weapon
        digitalWrite(Weapon, LOW);  // Low voltage to disengage weapon
        break;
      default:  // Default case does nothing
        break;
    }
  }
}
