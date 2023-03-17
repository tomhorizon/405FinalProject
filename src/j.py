import pyb
from motor_driver2 import MotorDriver2
from Servo import Servo

motor1Pin1 = pyb.Pin.board.PB5
motor1Pin2 = pyb.Pin.board.PA10
motor1Ena = pyb.Pin.board.PB3
motor1Tim = 2
motor1Ch1 = 2

motor2Pin1 = pyb.Pin.board.PA1
motor2Pin2 = pyb.Pin.board.PC1
motor2Ena = pyb.Pin.board.PA0
motor2Tim = 5
motor2Ch1 = 1

servoPin = pyb.Pin.board.PC9
servoTim = 3
servoCh = 4

motor1 = MotorDriver2(motor1Pin1, motor1Pin2, motor1Ena, motor1Tim, motor1Ch1)
motor2 = MotorDriver2(motor2Pin1, motor2Pin2, motor2Ena, motor2Tim, motor2Ch1)
servo = Servo(servoPin, servoTim, servoCh)

motor1.set_duty_cycle(0)
motor2.set_duty_cycle(0)

dirX = pyb.ADC(pyb.Pin.board.PC3)
dirY = pyb.ADC(pyb.Pin.board.PC0)

while True:
    valX = (dirX.read() - 2015)/20
    valY = (dirY.read() - 2040)/20
    if abs(valX) > 100:
        if valX > 0:
            valX = 100
        else:
            valX = -100
    if abs(valY) > 100:
        if valY > 0:
            valY = 100
        else:
            valY = -100
    if abs(valX) < 5:
         valX = 0
    if abs(valY) < 5:
        valY = 0
    
    print(f"X: {valX}\t Y: {valY}")
    motor1.set_duty_cycle(valX)
    pyb.delay(5)
    motor2.set_duty_cycle(-jj
                          valY)
    pyb.delay(5)