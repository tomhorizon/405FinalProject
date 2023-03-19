import pyb
from motor_driver2 import MotorDriver2
from Servo import Servo
from fireLED import FireLED
from buzzer import Buzzer
from goButton import GoButton

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

flywheelPin1 = pyb.Pin.board.PC5
flywheelPin2 = pyb.Pin.board.PB8
flywheelEna = pyb.Pin.board.PC8
flywheelTim = 3
flywheelCh = 3

servoPin = pyb.Pin.board.PC9
servoTim = 3
servoCh = 4

buzzerPin = pyb.Pin.board.PA9
buzzerTimer = 1
buzzerChannel = 2

goButtonPin = pyb.Pin.board.PA15

LEDpin = pyb.Pin.board.PA8
LEDtimer = 1
LEDchannel = 1

motor1 = MotorDriver2(motor1Pin1, motor1Pin2, motor1Ena, motor1Tim, motor1Ch1)
motor2 = MotorDriver2(motor2Pin1, motor2Pin2, motor2Ena, motor2Tim, motor2Ch1)
flywheel = MotorDriver2(flywheelPin1, flywheelPin2, flywheelEna, flywheelTim, flywheelCh)
servo = Servo(servoPin, servoTim, servoCh)
LED = FireLED(LEDpin, LEDtimer, LEDchannel)
alarm = Buzzer(buzzerPin, buzzerTimer, buzzerChannel)
goButton = GoButton(goButtonPin)

motor1.set_duty_cycle(0)
motor2.set_duty_cycle(0)
flywheel.set_duty_cycle(8)
LED.on()

dirX = pyb.ADC(pyb.Pin.board.PC3)
dirY = pyb.ADC(pyb.Pin.board.PC0)

switchOld = 0
alarm.numBeep(3)

while True:
    # read joystick values and scale, saturate
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

    # set motor values
    print(f"X: {valX}\t Y: {valY}")
    motor1.set_duty_cycle(valX)
    pyb.delay(5)
    motor2.set_duty_cycle(-valY)
    pyb.delay(5)

    # read bush button and determine if it has changed
    switchNew = goButton.value()
    pyb.delay(5)
    # print(switchNew)

    # engage or disengage firing servo as needed
    if switchNew != switchOld:
        #print(switchNew)
        if switchNew == 1:
            servo.engage()
            LED.hunt()
            alarm.on()

        else:
            servo.disengage()
            LED.on()
            alarm.off()
            
    switchOld = switchNew

