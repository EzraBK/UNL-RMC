import socket
from roboclaw import Roboclaw
from time import sleep

def main():
	global serverSocket
	serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	serverSocket.bind(("192.168.1.186", 6666))
	
	global roboclaw
	roboclaw = Roboclaw("/dev/serial0", 38400)
	roboclaw.Open()
	
	global LeftDrive, RightDrive, LinActuators, Chainsaw
	LeftDrive = 0x80
	RightDrive = 0x81
	LinActuators = 0x82
	Chainsaw = 0x83
	
	while True:
		loop()

def loop():
	data, addr = serverSocket.recvfrom(5)
	
	Drive(ord(data[0]), ord(data[1]))
	Dig(ord(data[2]))
#	LinUp(ord(data[3]))
#	LinDown(ord(data[4]))
	print(type(data))
	print(data[0])

def Driving(data):
	while roboclaw.out_waiting > 0:
		pass
	
	LeftDrive, RightDrive = Drive(ord(data[0]), ord(data[1]))
	
	print ("\nLeft Speed: ", LeftDrive, "\tRight Speed", RightDrive)
	

def Drive(Left, Right):
	if Left < 0 and Right < 0:
		roboclaw.ForwardMixed(LeftDrive, -(Left))
		roboclaw.ForwardMixed(RightDrive, -(Right))
	if Left < 0 and Right > 0:
		roboclaw.ForwardMixed(LeftDrive, -(Left))
		roboclaw.BackwardMixed(RightDrive, Right)
	if Left > 0 and Right < 0:
		roboclaw.BackwardMixed(LeftDrive, Left)
		roboclaw.ForwardMixed(RightDrive, -(Right))
	if Left > 0 and Right > 0:
		roboclaw.BackwardMixed(LeftDrive, Left)
		roboclaw.BackwardMixed(RightDrive, Right)

def Dig(digornodig):
	if (digornodig == 1):	#if the chainsaw button is pressed start the chainsaw
		roboclaw.ForwardMixed(Chainsaw, 127)
	else:					#if the chainsaw button is not pressed leave the chainsaw off
		roboclaw.ForwardMixed(Chainsaw, 0)


main()



