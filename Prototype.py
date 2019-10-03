import pygame
from roboclaw import Roboclaw
from time import sleep

LeftDrive = 0x80 #Channel 7 M1=Back Left  _  M2=Front Left
RightDrive = 0x81 #Channel 8 M1=Back Right  _  M2=Front Right
LinearActuators = 0x82 #Channel 9  - These MUST be moving at the same time!
BigAssChainsaw = 0x83 #Channel 10 - M1

roboclaw = Roboclaw("/dev/serial0", 38400)
roboclaw.Open()
pygame.init()
pygame.joystick.init()

if not pygame.joystick.get_count():
    print("\nPlease connect a joystick.\n")
    quit()
    
joystick = pygame.joystick.Joystick(0)
joystick.init()

Speed = 0
valueS = 0
SpeedT = 0
valueT = 0
Button0 = joystick.get_button( 0 )
Button1 = joystick.get_button( 1 )
Button2 = joystick.get_button( 2 )
Button3 = joystick.get_button( 3 )
Button4 = joystick.get_button( 4 )
Button5 = joystick.get_button( 5 )
Axis0 = joystick.get_axis( 0 )
Axis1 = joystick.get_axis( 1 )

while 1:
    print (Axis1)
 
 
 
# -------- Main Program Loop -----------
while (1):
    # EVENT PROCESSING STEP
    for event in pygame.event.get(): # User did something
        if event.type == pygame.JOYBUTTONDOWN:
            print("Joystick button pressed.")
        if event.type == pygame.JOYBUTTONUP:
            print("Joystick button released.")
            
	    

    while Button2 == 1:
	  roboclaw.ForwardM2(LinearActuators,127)
  	  roboclaw.ForwardM1(LinearActuators,127)
	  print("Linear Actuators Up")
	  if Button2 == 0:
	     roboclaw.ForwardM1(LinearActuators,0)
	     roboclaw.ForwardM2(LinearActuators,0)
	  break
		
		

    while Button3 == 1:
          roboclaw.BackwardM1(LinearActuators,127)
          roboclaw.BackwardM2(LinearActuators,127)
	  print("Linear Actuators Down")
	  if Button3 == 0:
	     roboclaw.BackwardM1(LinearActuators,0)
	     roboclaw.BackwardM2(LinearActuators,0)
	  break    
	
	
	
    while Button0 == 1:
	  roboclaw.ForwardM1(BigAssChainsaw, 127)
	  print("Start of Death Device")
	  if (Button0 == 0):
	      roboclaw.ForwardM1(BigAssChainsaw, 0)
	  break
            
	    
	    
    while Axis1 > .105:
	    Speed = Axis1
	    valueS = int(round(Speed * 127))
	    roboclaw.BackwardM1(LeftDrive, valueS)
	    roboclaw.BackwardM2(LeftDrive,valueS)
	    roboclaw.BackwardM1(RightDrive,valueS)
	    roboclaw.BackwardM2(RightDrive,valueS)
	    print("RETREAT! %d" % (Speed))
	    print(valueS)
	    if Axis1 < .105:
		roboclaw.BackwardM1(LeftDrive, 0)
		roboclaw.BackwardM2(LeftDrive, 0)
		roboclaw.BackwardM1(RightDrive, 0)
		roboclaw.BackwardM2(RightDrive, 0)
	    break
	    


    while Axis1 < -.105:
	    Speed = Axis1
	    valueS = int(round(Speed * -127))
	    roboclaw.ForwardM1(LeftDrive, valueS)
	    roboclaw.ForwardM2(LeftDrive,valueS)
	    roboclaw.ForwardM1(RightDrive,valueS)
	    roboclaw.ForwardM2(RightDrive,valueS)
	    print("CHARGE! %d" % (Speed))
	    print(valueS)
	    if Axis1 > -.105:
		roboclaw.BackwardM1(LeftDrive, 0)
		roboclaw.BackwardM2(LeftDrive, 0)
		roboclaw.BackwardM1(RightDrive, 0)
		roboclaw.BackwardM2(RightDrive, 0)

	    break   
	    



    while Button4 == 1:
	  roboclaw.BackwardM1(RightDrive, 90)
	  roboclaw.BackwardM2(RightDrive, 90)
	  roboclaw.ForwardM1(LeftDrive, 90)
	  roboclaw.ForwardM2(LeftDrive, 90)
	  print("Turn Left you idiot")
	  if Button4 == 0:
	     roboclaw.BackwardM1(LeftDrive, 0)
	     roboclaw.BackwardM2(LeftDrive, 0)
	     roboclaw.BackwardM1(RightDrive, 0)
	     roboclaw.BackwardM2(RightDrive, 0)
	  break




    while Button5 == 1:
	  roboclaw.BackwardM1(LeftDrive, 90)
	  roboclaw.BackwardM2(LeftDrive, 90)
	  roboclaw.ForwardM1(RightDrive, 90)
	  roboclaw.ForwardM2(RightDrive, 90)
	  print("Turn Right you jackass")
	  if Button5 == 0:
	     roboclaw.BackwardM1(LeftDrive, 0)
	     roboclaw.BackwardM2(LeftDrive, 0)
	     roboclaw.BackwardM1(RightDrive, 0)
	     roboclaw.BackwardM2(RightDrive, 0)
	  break

