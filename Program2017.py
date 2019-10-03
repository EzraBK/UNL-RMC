from __future__ import print_function
import pygame
import sys, os
import socket
import time

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

joy = None
count1 = 0
millis = 0
augerSpeed = 64
augerOn = True

#ethernet ip address
#ip = "192.168.137.38"
#wireless ip address
#ip = "192.168.137.37"
#raspberry pi 1
ip = "192.168.137.39"


def handleJoyEvent(e):
    if e.type == pygame.JOYBUTTONDOWN:
        if e.dict['button'] == 0:
            print("bye")
            quit()
        else:
            print("other button")
    else:
        print(e.type)

    #elif e.type == pygame.JOYAXISMOTION:
    #    print(e.dict['axis'])


def filterAxis(val):
    if abs(val) < .1:
        return 64
    else:
        if val < 0:
            val += .1
        else:
            val -= .1
        
        return int(val*70 + 64)
        

def loop():
    #check for button press
    #e = pygame.event.poll()
    #if e.type != pygame.NOEVENT:
    #    handleJoyEvent(e)
    pygame.event.pump()

    xAxis = filterAxis(joy.get_axis(0))
    yAxis = filterAxis(joy.get_axis(1)*-1)
    buttons = joy.get_button(0)
    buttons = buttons << 1
    buttons += joy.get_button(3)
    buttons = buttons << 1
    buttons += joy.get_button(1)
    buttons = buttons << 1
    buttons += joy.get_button(2)
    
    buttons2 = int(joy.get_axis(2) > .5)
    buttons2 = buttons2 << 1
    buttons2 += int(joy.get_axis(2) < -.5)
    buttons2 = buttons2 << 1
    buttons2 += joy.get_button(4)
    buttons2 = buttons2 << 1
    buttons2 += joy.get_button(5)
    buttons2 = buttons2 << 1
    buttons2 += joy.get_button(6)
    buttons2 = buttons2 << 1
    buttons2 += joy.get_button(7)
     
    global augerSpeed, augerOn, count1
    augerSpeed += joy.get_button(1)
    augerSpeed -= joy.get_button(2)
    
    augerSpeed =   1 if augerSpeed <   1 else augerSpeed
    augerSpeed = 127 if augerSpeed > 127 else augerSpeed
    
    if joy.get_button(9) and count1 > 10:
        augerOn = not augerOn
        count1 = 0
    
    augerVal = augerSpeed if augerOn else 64
    print(augerVal)
    
    
    #print(buttons, " ", bin(buttons))
    #print("Button {:>2} value: {}".format(0,button), end=" ")
    #print(joy.get_button(0), joy.get_button(1), joy.get_button(2), joy.get_button(3), joy.get_button(4), joy.get_button(5), joy.get_button(6), joy.get_button(7), True, False)
    #print(xAxis, "\t", yAxis)
    
    '''
    global count1, millis
    count1 += 1
    if count1 == 100:
        millis = int(time.time()*1000)
    if count1 == 1010:
        print("time: ", int(time.time()*1000) - millis)
    '''
    
    client.sendto(unichr(xAxis) + unichr(yAxis) + unichr(buttons+64) + unichr(augerVal) + unichr(buttons2+64), (ip, 6666))
    time.sleep(0.05)
    count1 += 1


def main():
    print("Main started\n")
    
    global client
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #client.sendto("Hello World", (ip, 6666))
    #sys.exit(0);
    
    pygame.joystick.init()
    pygame.display.init()
    #pygame.event.set_allowed(None)
    #pygame.event.set_allowed(pygame.JOYBUTTONDOWN)

    if not pygame.joystick.get_count():
        print("\nPlease connect a joystick.\n")
        quit()

    print("\nController detected: ")
    print(pygame.joystick.get_count())

    global joy
    joy = pygame.joystick.Joystick(0)
    joy.init()

    
    count = 0
    while True:
        loop()



main()

 
