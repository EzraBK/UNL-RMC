import socket
from roboclaw import Roboclaw
import serial
from time import sleep
import subprocess
import sys, os
import RPi.GPIO as GPIO

def main():

 global client
 client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
 client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
 client.bind(('192.168.1.30',6666))
 client.settimeout(0.01)

 global roboclaw
 roboclaw = Roboclaw("/dev/serial0",38400)
 roboclaw.Open()

 global LeftDrive, RightDrive, LinActuators, Chainsaw, Extender
 LeftDrive = 0x80
 RightDrive = 0x81
 LinActuators = 0x82
 Chainsaw = 0x83
 Extender = 0x84

 GPIO.setmode(GPIO.BOARD)
 GPIO.setup(12, GPIO.OUT)


 while True:
  status = subprocess.call(['ping', '-c', '1', '-W', '1', '192.168.1.1'], stdout=open(os.devnull, 'w'))
  try:
   data, addr = client.recvfrom(8)
   

   if status == 0:
    GPIO.output(12, True)
    Drive(ord(data[0]), ord(data[1]))
    LinAct(ord(data[2]), ord(data[3]))
    #Dig(ord(data[4]), ord(data[5]))
    #Extend(ord(data[6]), ord(data[7]))
    print 'CONNECTED: ','LEFT: ',ord(data[0]), '   Right: ', ord(data[1]), '   LinActs: ', LinStat, '   ', ord(data[4]), ord(data[6]), ord(data[7]), '\n\n'

   else:
    Reset()
    GPIO.output(12, False)
    print 'DISCONNECTED'

  except socket.timeout:
   Reset()
   print 'PROGRAM ENDED'
   sys.exit()

def Reset():
 roboclaw.ForwardBackwardMixed(LeftDrive, 63)
 roboclaw.ForwardBackwardMixed(RightDrive, 63)
 roboclaw.ForwardMixed(LinActuators, 0)
 roboclaw.ForwardMixed(Chainsaw, 0)

def Drive(LeftSpeed, RightSpeed):							#LeftJoystick-> LeftDrive --  RightJoysick-> RightDrive
 roboclaw.ForwardBackwardMixed(LeftDrive, LeftSpeed)		#
 roboclaw.LeftRightMixed(LeftDrive, 63)						#<-|
 roboclaw.ForwardBackwardMixed(RightDrive, RightSpeed)		#  |-- these need to be here becuase roboclaw is stupid
 roboclaw.LeftRightMixed(RightDrive, 63) 					#<-|    (but maybe not too stupid)

def LinAct(UP, DOWN):										#
 global LinStat												#Tells us what actuators are doing
 if UP == 1:												#Y_button-> UP
  roboclaw.BackwardMixed(LinActuators, 127)					#
  roboclaw.LeftRightMixed(LinActuators, 63)					#roboclaw is stupid
  LinStat = 'UP'											#
 elif DOWN == 1:											#B_button-> DOWN
  roboclaw.ForwardMixed(LinActuators, 127)					#
  roboclaw.LeftRightMixed(LinActuators, 63)					#roboclaw is stupid
  LinStat= 'DOWN'											#
 elif UP == 0 and DOWN == 0:								#
  roboclaw.BackwardMixed(LinActuators, 0)					#
  LinStat = 'NEUTRAL'										#
 

def Dig(ChainSpeed, Creep):									#
 global DigStat												#tells us what chainsaw is doing
 roboclaw.ForwardMixed(Chainsaw, ChainSpeed)				#
 roboclaw.LeftRightMixed(Chainsaw, 63)						#roboclaw is stupid
 if ChainSpeed > 0:											#
  DigStat = 'Digging: Do NOT use joystick'					#ChainSpeed is mapped to Left Trigger for variable speed
 else:														#
  DigStat = 'Not Digging'									#Creep mapped to A_button. Drives forward at low nonvariable speed
 if Creep == 1:												#while digging. Can be removed
  roboclaw.ForwardMixed(LeftDrive, 20)						#
  roboclaw.LeftRightMixed(LeftDrive, 63)					#roboclaw is stupid
  roboclaw.ForwardMixed(RightDrive, 20)						#
  roboclaw.LeftRightMixed(RightDrive, 63)					#roboclaw is stupid

def Extend(EXTEND, RETRACT):
 global ExStat
 if EXTEND == 1:
  roboclaw.ForwardM1(Extender, 127)
  ExStat = 'EXTENDING'
 elif RETRACT == 1:
  roboclaw.BackwardM1(Extender, 127)
  ExStat = 'RETRACTING'
 elif EXTEND == 0 and RETRACT == 0:
  roboclaw.BackwardM1(Extender, 0)
  ExStat =  'NEUTRAL'

main()
