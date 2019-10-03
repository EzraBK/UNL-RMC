import pygame
from roboclaw import Roboclaw
from time import sleep

LeftDrive = 0x80 #Channel 7 M1=Back Left  _  M2=Front Left
RightDrive = 0x81 #Channel 8 M1=Back Right  _  M2=Front Right
LinearActuators = 0x82 #Channel 9  - These MUST be moving at the same time!
BigAssChainsaw = 0x83 #Channel 10 - M1
DButton = 0
LAButtonU = 0
LAButtonD = 0
JoystickDrive = 0
Speed = 0
valueS = 0
SpeedT = 0
valueT = 0
JoystickDriveB = 0
TurnR = 0
TurnL = 0
hat = 0
hats = 0

roboclaw = Roboclaw("/dev/serial0", 38400)
roboclaw.Open()
pygame.init()
pygame.joystick.init()
joystick_count = pygame.joystick.get_count()
joystick = pygame.joystick.Joystick(0)
joystick.init()
name = joystick.get_name()
axes = joystick.get_numaxes()
 
 
 
# -------- Main Program Loop -----------
while (1):
    # EVENT PROCESSING STEP
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop
        
        # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
        if event.type == pygame.JOYBUTTONDOWN:
            print("Joystick button pressed.")
        if event.type == pygame.JOYBUTTONUP:
            print("Joystick button released.")
            
	    
	    
    
    if joystick.get_button( 2 ) == 1:
	LAButtonU = 1
    while (LAButtonU == 1):
	  roboclaw.ForwardM2(LinearActuators,127)
  	  roboclaw.ForwardM1(LinearActuators,127)
	  print("Linear Actuators Up")
	  if joystick.get_button( 2 ) == 0:
	     roboclaw.ForwardM1(LinearActuators,0)
	     roboclaw.ForwardM2(LinearActuators,0)
	     LAButtonU = 0
	  break
		
		
		
    if joystick.get_button( 3 ) == 1:
	LAButtonD = 1
    while (LAButtonD == 1):
          roboclaw.BackwardM1(LinearActuators,127)
          roboclaw.BackwardM2(LinearActuators,127)
	  print("Linear Actuators Down")
	  if joystick.get_button( 3 ) == 0:
	     roboclaw.BackwardM1(LinearActuators,0)
	     roboclaw.BackwardM2(LinearActuators,0)
	     LAButtonD = 0
	  break    
	
	
		
    if (joystick.get_button( 0 ) == 1):
	DButton = 1
    while (DButton == 1):
	  roboclaw.ForwardM1(BigAssChainsaw, 127)
	  print("Start of Death Device")
	  if (joystick.get_button( 0 ) == 0):
	      roboclaw.ForwardM1(BigAssChainsaw, 0)
	      DButton = 0
	  break
            
            
    if (joystick.get_axis( 1 ) > .105):
	JoystickDrive = 1
    while (JoystickDrive == 1):
	    Speed = (joystick.get_axis( 1 ))
	    valueS = int(round(Speed * 127))
	    roboclaw.BackwardM1(LeftDrive, valueS)
	    roboclaw.BackwardM2(LeftDrive,valueS)
	    roboclaw.BackwardM1(RightDrive,valueS)
	    roboclaw.BackwardM2(RightDrive,valueS)
	    print("RETREAT! %d" % (Speed))
	    print(valueS)
	    if (joystick.get_axis( 1 ) < .105):
		roboclaw.BackwardM1(LeftDrive, 0)
		roboclaw.BackwardM2(LeftDrive, 0)
		roboclaw.BackwardM1(RightDrive, 0)
		roboclaw.BackwardM2(RightDrive, 0)
		JoystickDrive = 0
	    break
	    
    if (joystick.get_axis( 1 ) < -.105):
	JoystickDriveB = 1
    while (JoystickDriveB == 1):
	    Speed = (joystick.get_axis( 1 ))
	    valueS = int(round(Speed * -127))
	    roboclaw.ForwardM1(LeftDrive, valueS)
	    roboclaw.ForwardM2(LeftDrive,valueS)
	    roboclaw.ForwardM1(RightDrive,valueS)
	    roboclaw.ForwardM2(RightDrive,valueS)
	    print("CHARGE! %d" % (Speed))
	    print(valueS)
	    if (joystick.get_axis( 1 ) > -.105):
		roboclaw.BackwardM1(LeftDrive, 0)
		roboclaw.BackwardM2(LeftDrive, 0)
		roboclaw.BackwardM1(RightDrive, 0)
		roboclaw.BackwardM2(RightDrive, 0)
		JoystickDriveB = 0
	    break   
	    
    if joystick.get_button( 4 ) == 1:
	TurnL = 1
    while (TurnL == 1):
	  roboclaw.BackwardM1(RightDrive, 90)
	  roboclaw.BackwardM2(RightDrive, 90)
	  roboclaw.ForwardM1(LeftDrive, 90)
	  roboclaw.ForwardM2(LeftDrive, 90)
	  print("Turn Left you idiot")
	  if joystick.get_button( 4 ) == 0:
	     roboclaw.BackwardM1(LeftDrive, 0)
	     roboclaw.BackwardM2(LeftDrive, 0)
	     roboclaw.BackwardM1(RightDrive, 0)
	     roboclaw.BackwardM2(RightDrive, 0)
	     TurnL = 0
	  break

    if joystick.get_button( 5 ) == 1:
	TurnR = 1
    while (TurnR == 1):
	  roboclaw.BackwardM1(LeftDrive, 90)
	  roboclaw.BackwardM2(LeftDrive, 90)
	  roboclaw.ForwardM1(RightDrive, 90)
	  roboclaw.ForwardM2(RightDrive, 90)
	  print("Turn Right you jackass")
	  if joystick.get_button( 5 ) == 0:
	     roboclaw.BackwardM1(LeftDrive, 0)
	     roboclaw.BackwardM2(LeftDrive, 0)
	     roboclaw.BackwardM1(RightDrive, 0)
	     roboclaw.BackwardM2(RightDrive, 0)
	     TurnR = 0
	  break

		
