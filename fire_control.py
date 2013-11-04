#!/usr/bin/python
#
# Airsoft Turret Fire Control
#
# Author: Adam Meyers (madboo@d0ubletap.net)
#
# This code sends serial instructions to the Arduino Controller for the 
# Airsoft Turret. There are three exported function from this class:
#   Sendcoord - move the turret to a given X,Y position
#    Input: cmd, x, y - the command should be 0xFF
#    Output: 1 for succesful move, or a message that indicates the move didn't occur
#   Fire - Fire a 500ms burst
#    Input: cmd - the command should be 0xFE
#    Output: None
#   Close - Gracefully close the serial connection
#    Input: None
#    Output: None


# Import Serial library for arduino control and struct to pack bytes for transmission to the device.
import serial
from struct import * 

class fire_control:
# This class is instantiated as a control object in the monitor.py code

  def __init__(self):
# Initialize the serial connection - this connection is maintained in init as initializing on movement create overhead
    self.ser = serial.Serial('/dev/ttyACM0',9600)  #Default serial interface
    print "Connecting to Arduino" # Provide output that connection is occuring
    print self.ser.readline() # Arduino should notify us when its conencted


  def sendcoord(self,cmd,x,y):
# This function receives the command to send, and the x,y positions this will be packed into bytes and sent over the serial connection returning 1 if the command was sent. A govenor will prevent movement outside of the defined ranges which corresponds to the visibility of the webcam for motion.
    bytes = [cmd,x,y] # The command structure to be sent
    if ((x > 46) and (x < 136) and (y > 41) and (y < 130)): # Govenor
      print "Sending Bytes: ",bytes
      self.ser.write(pack(">3B",cmd,x,y)) # Pack the command and coord into a 3 byte buffer
      return 1 # Successful movement - return 1
    else:
      return "Out of Range" # Out of range message

  def fire(self,cmd):
# This function receives the fire command and packs it into a one byte buffer thish is transmitted to the arduino
    print "Fire!: ",cmd
    self.ser.write(pack(">B",cmd)) # Pack command

  def close(self): 
# This function will disconnect the Arduino serial connection
    self.ser.close() # Disconnect the Arduino serial connection
   

def main():
# This is the main function which will be called if the fire_controll program is called as a standalone. This will primarily be used to quickly test the fire control program by moving the turret slightly to the right and pitch the weapon at 90 degrees. It will then fire a 500ms burst.
  print "test pattern"
  fc = fire_control() # Instantiate a new fire_control object
#  Left most angle
#  fc.sendcoord(0xff,76,90)
  fc.sendcoord(0xff,106,90) # Send the coordinates to move the turret
  fc.fire(0xfe) # Fire a 500ms burst
  fc.close() # Gracefully close the serial connection

if __name__=='__main__':
  main()
