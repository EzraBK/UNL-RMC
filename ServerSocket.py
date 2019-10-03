import serial
import socket
import RPi.GPIO as GPIO


def main():
    global serverSocket
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serverSocket.bind(("192.168.137.39", 6666))

    global roboclaw
    roboclaw = serial.Serial('/dev/ttyAMA0', 38400)
    
    global motorDrive, motorActua, motorAuger, motorDumpp
    motorDrive = 29     #1: left drive motors, 2: right drive motors
    
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(motorDrive, GPIO.OUT)

    while True:
        loop()


def loop():
    data, addr = serverSocket.recvfrom(5)
    #print "received: ", data,

    driveMotor(data)
    print " "


def driveMotor(data):
    while roboclaw.out_waiting > 0:
        pass
    #drive motors
    GPIO.output(motorDrive, True)

    leftSpeed, rightSpeed = arcadeDrive(ord(data[0]), ord(data[1]))

    roboclaw.write(chr(leftSpeed))
    while roboclaw.out_waiting > 0:
        pass
    roboclaw.write(chr(rightSpeed))
    print "Left: ", leftSpeed, "\tRight: ", rightSpeed,


def arcadeDrive(xAxis, yAxis):
    xAxis -= 64
    leftSpeed = lim(yAxis - xAxis)
    rightSpeed = lim(yAxis + xAxis)
    
    return (leftSpeed, rightSpeed+128)

def lim(speed):
    if speed < 1:
        speed = 1
    elif speed > 127:
        speed = 90

    return speed


if __name__ == "__main__":
    main()




    

