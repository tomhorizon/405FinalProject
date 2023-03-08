import pyb
import utime as time
import gc
from motor_driver2 import MotorDriver2
from encoder_reader import EncoderReader
from control import Control
#from mlx_cam import MLX_Cam
from machine import Pin, I2C

#Imports for MLX_Cam stuff
# import gc
import array
#import utime as time
from machine import Pin, I2C
from mlx90640 import MLX90640
# from mlx90640 import RefreshRate
from mlx90640.calibration import NUM_ROWS, NUM_COLS, IMAGE_SIZE, TEMP_K
from mlx90640.image import ChessPattern, InterleavedPattern

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
motor1 = MotorDriver2(motor1Pin1, motor1Pin2, motor1Ena, motor1Tim, motor1Ch1)
motor2 = MotorDriver2(motor2Pin1, motor2Pin2, motor2Ena, motor2Tim, motor2Ch1)
encoder1 = EncoderReader(encoder1Pin1, encoder1Pin2, encoder1Tim, encoder1Ch1, encoder1Ch2)
encoder2 = EncoderReader(encoder2Pin1, encoder2Pin2, encoder2Tim, encoder2Ch1, encoder2Ch2)

def main(setPoint1, setPoint2):
    KP1 = .15
    KP2 = .15
    
    control1 = Control(KP1, setPoint1 + 32768)
    control2 = Control(KP2, setPoint2 + 32768)
    
    encoder1.zero()
    encoder2.zero()
    
    elapsed = 0
    startTime = time.ticks_ms()
    
    while elapsed <= 3000:
        currentTime = time.ticks_ms()
        elapsed = currentTime - startTime

        pos1 = encoder1.read()
        psi1 = control1.run(pos1)
        motor1.set_duty_cycle(-psi1)
        pyb.delay(5)
        
        pos2 = encoder2.read()
        psi2 = control2.run(pos2)
        motor2.set_duty_cycle(-psi2)
        pyb.delay(5)
        
        #print(psi1, psi2)
          print("done")
    motor1.set_duty_cycle(0)
    motor2.set_duty_cycle(0)


if __name__ == "__main__":
    while 1:
        #yaw: pos CCW, neg CW
        #pitch: pos down, neg up
        
        setPoint1, setPoint2 = 2000, 500
        
        
        print(setPoint1, setPoint2)
        main(setPoint1, setPoint2)
        pyb.delay(1000)
        print(-setPoint1, -setPoint2)
        main(-setPoint1, -setPoint2)
        pyb.delay(1000)
