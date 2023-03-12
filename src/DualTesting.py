# First Dual Testing File
import pyb
import utime as time
import gc
gc.collect()
from motor_driver2 import MotorDriver2
from encoder_reader import EncoderReader
from control import Control
from machine import Pin, I2C
import array
from mlx90640 import MLX90640
from mlx90640.calibration import NUM_ROWS, NUM_COLS, IMAGE_SIZE, TEMP_K
from mlx90640.image import ChessPattern, InterleavedPattern
from mlx_cam import MLX_Cam
from Servo import Servo
from flyhweel import Flywheel
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

def initialize():
    alarm.powerUp()
    LED.powerUp()
    entry = input("Enter to start shakedown. Turn on High Voltage Power before continuing.\nEnsure turret is level and safe to rotate.")
    
    print("Testing Servo.")
    servo.powerUp()
    
    print("Testing flywheels.")
    flywheel.set_duty_cycle(0)
    flywheel.set_duty_cycle(3)
    pyb.delay(500)
    flywheel.set_duty_cycle(0)
    
    print("Testing yaw motor.")
    motor1.set_duty_cycle(-25)
    pyb.delay(250)
    motor1.set_duty_cycle(25)
    pyb.delay(250)
    motor1.set_duty_cycle(0)
    pyb.delay(250)
    
#     for i in range(1000):
#         motor1.set_duty_cycle(20*sin(2*3.1415/(i*+1)))
#         pyb.delay(10)
    
    print("Testing pitch motor.")
    motor2.set_duty_cycle(-25)
    pyb.delay(250)
    motor2.set_duty_cycle(25)
    pyb.delay(250)
    motor2.set_duty_cycle(0)
    pyb.delay(250)
    
    print("Shakedown complete.")
    
def dual():
    initTime = time.ticks_ms()
    try:
        from pyb import info
    # Oops, it's not an STM32; assume generic machine.I2C for ESP32 and others
    except ImportError:
        # For ESP32 38-pin cheapo board from NodeMCU, KeeYees, etc.
        i2c_bus = I2C(1, scl=Pin(22), sda=Pin(21))
    # OK, we do have an STM32, so just use the default pin assignments for I2C1
    else:
        i2c_bus = I2C(2)    # Keep this at 2 - had to change some pins around, i2c2 works
    # Select MLX90640 camera I2C address, normally 0x33, and check the bus
    i2c_address = 0x33
    scanhex = [f"0x{addr:X}" for addr in i2c_bus.scan()]
    gc.collect()
    camera = MLX_Cam(i2c_bus)
    gc.collect()
    
    encoder1.zero()
    encoder2.zero()
    
    flywheel.set_duty_cycle(3)
    
    KP1 = .15
    KP2 = .15
    
#     setPoint1 = -6400
    setPoint1 = 0 # just testing on my desk an don't want it rotating lol
    setPoint2 = 0
     
    motor1.set_duty_cycle(0)
    motor2.set_duty_cycle(0)
    pyb.delay(500)
    gc.collect()
    print("Power On")
    pyb.delay(1000)
    control1 = Control(KP1, setPoint1 + 32768)
    control2 = Control(KP1, setPoint2 + 32768)
    psi1 = 101
    elapsed = 0
    startTime = time.ticks_ms()
#     while (abs(psi1) > 10):
    LED.hunt()
    while (elapsed < 3000):
        elapsed = time.ticks_ms() - startTime
        pos1 = encoder1.read()
        pos2 = encoder2.read()
        psi1 = control1.run(pos1)
        motor1.set_duty_cycle(-psi1)
        pyb.delay(5)
        
        psi2 = control2.run(pos2)
        motor2.set_duty_cycle(-psi2)
        pyb.delay(5)
    
    motor1.set_duty_cycle(0)
    motor2.set_duty_cycle(0)
    xrange = [6, 26]
    gc.collect()
    yaw_sum = 0
    pitch_sum = 0
    print(f"Elapsed: {time.ticks_ms() - initTime}")
    servo.magDump(1)
    #while ((time.ticks_ms() - initTime) < 5000):
    image = camera.get_image()   #freezing here, it was working before?? wtf
    print("a")
    camera.ascii_art(image)
    print("b")
    Yaw_error, Pitch_error = camera.target_alg(xrange)
    print("c")
    setPoint1 = Yaw_error*61
    setPoint2 = Pitch_error*61
    
    print(f"Yaw_e = {Yaw_error}, Pitch_e = {Pitch_error}")
    control1 = Control(KP1, setPoint1 + 32768)
    control2 = Control(KP2, setPoint2 + 32768)
    
    encoder1.zero()
    encoder2.zero()
    elapsed = 0
    startTime = time.ticks_ms()
    
    psi2 = 51
    KP1 = .15
    KP2 = .15
#     while (abs(psi2) > 2):
    while (elapsed < 1000):
        elapsed = time.ticks_ms() - startTime
        pos1 = encoder1.read()
        pos2 = encoder2.read()
        psi1 = control1.run(pos1)
        motor1.set_duty_cycle(-psi1)
        alarm.beep(psi1)
        pyb.delay(5)
        
        psi2 = control2.run(pos2)
        motor2.set_duty_cycle(-psi2)
        pyb.delay(5)
        
    motor1.set_duty_cycle(0)
    motor2.set_duty_cycle(0)
    pyb.delay(20)
    alarm.off()
    LED.on()
    pyb.delay(20)
    servo.magDump(1)
    pyb.delay(20)
    LED.on()
    flywheel.set_duty_cycle(0)
    
#     print("shoot")
#     pyb.delay(500)
#     flywheel.murder(0)
    print("Target Engaged")
    
if __name__ == "__main__":
#     servo.fire()
#     LED.on()
#     alarm.beep(50)
#     pyb.delay(500)
#     LED.off()
#     alarm.alarmOff()
    initialize()
    entry = input("Waiting for go ahead. TURN OFF MAIN POWER BEFORE ABORTING.")
    dual()
    entry = input("Waiting for end. TURN OFF MAIN POWER BEFORE RESETTING.")
    