import pygame
import socket
import sys, os
from time import sleep

#----Axes--------       --------Buttons---------------   -------Hat-------
#ForBack = 1			Tigger = 0		7 = 6				
#LeftRight = 0			JoySide = 1		8 = 7
#Paddle = 3			3 = 2			9 = 8		    		(0,1)
#Twist = 4			4 = 3			10 = 9			 (-1,0) DPAD (1,0)
#				5 = 4			11 = 10		       	   (0,-1)
#		 		6 = 5			12 = 11
#					[number on joystick = number in program]

global server
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

ip = '192.168.1.30'

pygame.joystick.init()
pygame.display.init()

global joy
joy = pygame.joystick.Joystick(0)
joy.init()




def filterAxis(val, axis):
	if axis == 0:
	 val = (val+1)/2*127
	elif axis == 1:
	 val = (-1*val+1)/2*127
	return int(val)
	
	
#def ChainsawFilter(val):
 #if val < 0:
  #val = -1*val*127
 #elif val >= 0:
  #val = val*127
 #return int(val)
 

 
 
 
while True:
 
  pygame.event.pump()
  
  LinUP = joy.get_button(3)
  LinDOWN = joy.get_button(2)
  LinUP_Left = joy.get_button(5)
  LinDOWN_Left = joy.get_button(4)
  LinUP_Right = joy.get_button(9)
  LinDOWN_Right = joy.get_button(8)
  Creep = joy.get_button(1)
  Extend = joy.get_button(5)
  Retract = joy.get_button(4)
  Conveyor = joy.get_button(0)
  Reset = joy.get_button(6)
  Start = joy.get_button(11)
  
  ForBack = filterAxis(joy.get_axis(1), 1)
  RightLeft = filterAxis(joy.get_axis(0), 0)
  ChainSpeed = filterAxis(joy.get_axis(2), 1)
 
  print(ForBack, RightLeft, LinUP, LinDOWN, ChainSpeed, Creep, Extend, Retract, Conveyor, Reset, LinDOWN_Left, LinUP_Left, LinDOWN_Right, LinUP_Right)
  
  server.sendto(bytes((ForBack, RightLeft, LinUP, LinDOWN, ChainSpeed, Creep, Extend, Retract, Conveyor, Reset, LinDOWN_Left, LinUP_Left, LinDOWN_Right, LinUP_Right)),(ip,6666))
  
  if joy.get_button(10) == 1:
   sys.exit() 
