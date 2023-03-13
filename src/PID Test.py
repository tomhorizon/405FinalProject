from control2 import Control2
from motor_driver2 import MotorDriver2
from encoder_reader import EncoderReader
import pyb
import utime as time

# motor constants
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

encoder1Pin1 = pyb.Pin.board.PB7
encoder1Pin2 = pyb.Pin.board.PB6
encoder1Tim = 4
encoder1Ch1 = 1
encoder1Ch2 = 2

encoder2Pin1 = pyb.Pin.board.PC6
encoder2Pin2 = pyb.Pin.board.PC7
encoder2Tim = 8
encoder2Ch1 = 1
encoder2Ch2 = 2

motor1 = MotorDriver2(motor1Pin1, motor1Pin2, motor1Ena, motor1Tim, motor1Ch1)
motor2 = MotorDriver2(motor2Pin1, motor2Pin2, motor2Ena, motor2Tim, motor2Ch1)
encoder1 = EncoderReader(encoder1Pin1, encoder1Pin2, encoder1Tim, encoder1Ch1, encoder1Ch2)
encoder2 = EncoderReader(encoder2Pin1, encoder2Pin2, encoder2Tim, encoder2Ch1, encoder2Ch2)

def loop(setPoint1, setPoint2):
    #setPoint1 = int(input("SP1:"))
    #setPoint2 = int(input("SP2:"))
    #entry = input("Hit Enter after power is on")
    
    KP1 = .008
    KI1 = .01
    KD1 = .0
    
    KP2 = .008
    KI2 = .015
    KD2 = .03
    
    motor1.set_duty_cycle(0)
    motor2.set_duty_cycle(0)
    encoder1.zero()
    encoder2.zero()
    
    control1 = Control2(KP1, KI1, KD1, setPoint1 + 32768)
    control2 = Control2(KP2, KI2, KD2, setPoint2 + 32768)
    pyb.delay(5)
    elapsed = 0
    startTime = time.ticks_ms()
    while (elapsed < 1000):
        elapsed = time.ticks_ms() - startTime
        pos1 = encoder1.read()
        pos2 = encoder2.read()
        
        psi1 = control1.run(pos1)
        psi2 = control2.run(pos2)
        
        motor1.set_duty_cycle(-psi1)
        motor2.set_duty_cycle(psi2)
        
        pyb.delay(5)
        
    motor1.set_duty_cycle(0)
    motor2.set_duty_cycle(0)
    
    #entry = input("done")
    
if __name__ == "__main__":
    entry = input("enter")
    while 1:
        print("Positive Values")
        loop(3000, 120)
        pyb.delay(500)
        
        print("Negative Values")
        loop(-3000, -120)
        pyb.delay(500)
    
