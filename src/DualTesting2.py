# First Dual Testing File
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
flywheel.set_duty_cycle(0)
motor1.set_duty_cycle(0)
motor2.set_duty_cycle(0)


KP1 = .009
KI1 = .021
KD1 = .01

KP2 = .008
KI2 = .015
KD2 = .03

def initialize():
    print("Booting up...")
    encoder1.zero()
    encoder2.zero()
    
    alarm.powerUp()
    LED.powerUp()
    
    entry = input("Enter to start shakedown. Turn on High Voltage Power before continuing.\nEnsure turret is level and safe to rotate.")
    servo.powerUp()
    flywheel.set_duty_cycle(0)
    flywheel.set_duty_cycle(3)
    pyb.delay(500)
    flywheel.set_duty_cycle(0)
    
    motor1.set_duty_cycle(-35)
    pyb.delay(200)
    motor1.set_duty_cycle(35)
    pyb.delay(200)
    motor1.set_duty_cycle(0)
    pyb.delay(100)
    
    motor2.set_duty_cycle(-25)
    pyb.delay(150)
    motor2.set_duty_cycle(25)
    pyb.delay(100)
    motor2.set_duty_cycle(0)
    pyb.delay(100)
    
    print("Shakedown complete.")
    flywheel.set_duty_cycle(5)
    
def dual():
    master_timer = time.ticks_ms()
    track_yaw = 0
    encoder1.zero()
    encoder2.zero()
    
    initTime = time.ticks_ms()
    i2c_bus = I2C(2) 
    i2c_address = 0x33
    camera = MLX_Cam(i2c_bus)
    print("Power On")
    motor1.set_duty_cycle(0)
    motor2.set_duty_cycle(0)
    LED.hunt()
    
    #changepain level here  (x / 100)
    flywheel.set_duty_cycle(5)

    # rotate 180 - seems to be around 7000
    # positive yaw: CCW
    # positive pitch: DOWN
    setPoint1 = 6300 # just testing on my desk an don't want it rotating lol
    setPoint2 = 0
    
    track_yaw = track_yaw + setPoint1
    
    psi1 = 101
    control1 = Control2(KP1, KI1, KD1, setPoint1 + 32768)
    pyb.delay(5)
    elapsed = 0
    start = time.ticks_ms()
    while (elapsed < 1500):
        elapsed = time.ticks_ms() - start
        pos1 = encoder1.read()
        psi1 = control1.run(pos1)
        motor1.set_duty_cycle(-psi1)
        pyb.delay(5)
        print(psi1)
        #psi1 = 0
        
    motor1.set_duty_cycle(0)
    motor2.set_duty_cycle(0)
    xrange = [6, 26]
    gc.collect()
    yaw_sum = 0
    pitch_sum = 0
    
    #change pain level here  (x / 100)
    flywheel.set_duty_cycle(12)
    pyb.delay(2000)
    
    elapsed = 0
    while elapsed < 5000:
        elapsed = time.ticks_ms() - master_timer
        pyb.delay(3)
    
    print("Click")
    image = camera.get_image()
    print("Image received")
    
    camera.ascii_art(image)
    Yaw_error, Pitch_error = camera.target_alg(xrange)
    setPoint1 = Yaw_error*61
    setPoint2 = Pitch_error*61
    
    track_yaw = track_yaw + setPoint1

    print(f"Yaw_e = {Yaw_error}, Pitch_e = {Pitch_error}")
    encoder1.zero()
    encoder2.zero()
    
    elapsed = 0
    psi1 = 101
    control1 = Control2(KP1, KI1, KD1, setPoint1 + 32768)
    control2 = Control2(KP2, KI2, KD2, setPoint2 + 32768)
    pyb.delay(5)
    start = time.ticks_ms()
    while (elapsed < 250):
        elapsed = time.ticks_ms() - start
        pos1 = encoder1.read()
        pos2 = encoder2.read()
        
        psi1 = control1.run(pos1)
        psi2 = control2.run(pos2)
        
        motor1.set_duty_cycle(-psi1)
        motor2.set_duty_cycle(psi2)
        
        alarm.beep(abs(psi1))
        pyb.delay(5)
        print(psi1)
        #psi1 = 0
        
    motor1.set_duty_cycle(0)
    motor2.set_duty_cycle(0)
    servo.magDump(1)
    
    LED.on()
    alarm.off()
    flywheel.set_duty_cycle(3)
    print("Target Engaged")
    
    
    encoder1.zero()
    encoder2.zero()
    
    control1 = Control2(KP1, KI1, KD1, -track_yaw + 32768)
    pyb.delay(5)
    elapsed = 0
    start = time.ticks_ms()
    while (elapsed < 1500):
        elapsed = time.ticks_ms() - start
        pos1 = encoder1.read()
        psi1 = control1.run(pos1)
        motor1.set_duty_cycle(-psi1)
        pyb.delay(5)
        print(psi1)
        #psi1 = 0
        
    motor1.set_duty_cycle(0)
    motor2.set_duty_cycle(0)

    
if __name__ == "__main__":
    initialize()
    entry = input("Waiting for go ahead. TURN OFF MAIN POWER BEFORE ABORTING.")
    dual()
    entry = input("Waiting for end. TURN OFF MAIN POWER BEFORE RESETTING.")
    