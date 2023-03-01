import pyb
import utime
from motor_driver import MotorDriver
from encoder_reader import EncoderReader
from control import Control

# motor constants
motor1Pin1 = pyb.Pin.board.PB4
motor1Pin2 = pyb.Pin.board.PB5
motor1Ena = pyb.Pin.board.PA10
motor1Tim = 3
motor1Ch1 = 1
motor1Ch2 = 2

motor2Pin1 = pyb.Pin.board.PA0
motor2Pin2 = pyb.Pin.board.PA1
motor2Ena = pyb.Pin.board.PC1
motor2Tim = 5
motor2Ch1 = 1
motor2Ch2 = 2

# encoder constants
encoder1Pin1 = pyb.Pin.board.PB6
encoder1Pin2 = pyb.Pin.board.PB7
encoder1Tim = 4
encoder1Ch1 = 1
encoder1Ch2 = 2
encoder2Pin1 = pyb.Pin.board.PC6
encoder2Pin2 = pyb.Pin.board.PC7
encoder2Tim = 8
encoder2Ch1 = 1
encoder2Ch2 = 2

# initialize motors and encoder objects
motor1 = MotorDriver(motor1Ena, motor1Pin1, motor1Pin2, motor1Tim, motor1Ch1, motor1Ch2)
motor2 = MotorDriver(motor2Ena, motor2Pin1, motor2Pin2, motor2Tim, motor2Ch1, motor2Ch2)
encoder1 = EncoderReader(encoder1Pin1, encoder1Pin2, encoder1Tim, encoder1Ch1, encoder1Ch2)
encoder2 = EncoderReader(encoder2Pin1, encoder2Pin2, encoder2Tim, encoder2Ch1, encoder2Ch2)


def main():
    KP1 = .1
    setPoint1 = 5000
    
    
    control1 = Control(KP1, setPoint1)
    
    print(f'{setPoint1}, {KP1}')
    
    encoder1.zero()

    elapsed = 0
    startTime = utime.ticks_ms()
    while 1:
        currentTime = utime.ticks_ms()
        elapsed = currentTime - startTime

        pos1 = encoder1.read()
        print(pos1)
        psi = control1.run(pos1)
        motor1.set_duty_cycle(psi)
        #print(psi)
        pyb.delay(10)
    

    motor1.set_duty_cycle(0)
    motor2.set_duty_cycle(0)

    

    
while True: 
    main()
    pyb.delay(10000)
