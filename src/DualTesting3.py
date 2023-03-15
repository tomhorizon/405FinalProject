# Third Dual Testing File
import pyb
import utime as time
import gc
gc.collect()
from motor_driver2 import MotorDriver2
from encoder_reader import EncoderReader
from control2 import Control2
from machine import Pin, I2C
import array
from mlx90640 import MLX90640
from mlx90640.calibration import NUM_ROWS, NUM_COLS, IMAGE_SIZE, TEMP_K
from mlx90640.image import ChessPattern, InterleavedPattern
from mlx_cam import MLX_Cam
from Servo import Servo
from fireLED import FireLED
from buzzer import Buzzer
from math import sin
from math import cos
from goButton import GoButton
from turret import Turret

gc.collect()
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
gc.collect()

# servo contants
servoPin = pyb.Pin.board.PC9
servoTim = 3
servoCh = 4

# buzzer constants
buzzerPin = pyb.Pin.board.PA9
buzzerTimer = 1
buzzerChannel = 2

# LED constants
LEDpin = pyb.Pin.board.PA8
LEDtimer = 1
LEDchannel = 1

# Flywheel constants
flywheelPin1 = pyb.Pin.board.PC5
flywheelPin2 = pyb.Pin.board.PB8
flywheelEna = pyb.Pin.board.PC8
flywheelTim = 3
flywheelCh = 3

goButtonPin = pyb.Pin.board.PA15

# initialize motors and encoder objects
#Motor 1 = Yaw. Motor 2 = Pitch
motor1 = MotorDriver2(motor1Pin1, motor1Pin2, motor1Ena, motor1Tim, motor1Ch1)
motor2 = MotorDriver2(motor2Pin1, motor2Pin2, motor2Ena, motor2Tim, motor2Ch1)
flywheel = MotorDriver2(flywheelPin1, flywheelPin2, flywheelEna, flywheelTim, flywheelCh)
encoder1 = EncoderReader(encoder1Pin1, encoder1Pin2, encoder1Tim, encoder1Ch1, encoder1Ch2)
encoder2 = EncoderReader(encoder2Pin1, encoder2Pin2, encoder2Tim, encoder2Ch1, encoder2Ch2)
servo = Servo(servoPin, servoTim, servoCh)
LED = FireLED(LEDpin, LEDtimer, LEDchannel)
alarm = Buzzer(buzzerPin, buzzerTimer, buzzerChannel)
goButton = GoButton(goButtonPin)
flywheel.set_duty_cycle(0)

# Initialize I2C Communication
i2c_bus = I2C(2) 
i2c_address = 0x33
camera = MLX_Cam(i2c_bus)

if __name__ == "__main__":
    
    turret = Turret(motor1, motor2, encoder1, encoder2, flywheel, servo, LED, alarm, camera, goButton)
    turret.wakeUp()

    while True:
        alarm.numBeep(1)
        print("Waiting for Button")
        while goButton.value() == 0:
            pyb.delay(3)
        alarm.powerUp()
        print("Button Pressed")

        initTime = time.ticks_ms()
        turret.yaw180()
        while time.ticks_ms() - initTime < 5000:
            pyb.delay(3)

        xrange = [6, 26]
        turret.findTarget(xrange)
        turret.aim()
        turret.fire(1)
        pyb.delay(50)
        turret.sleep()

