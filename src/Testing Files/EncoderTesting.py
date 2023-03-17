import pyb
import utime as time
import gc
gc.collect()
from motor_driver2 import MotorDriver2
from encoder_reader import EncoderReader
from control import Control
from mlx_cam import MLX_Cam
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

# buzzer constants
buzzerPin = pyb.Pin.board.PB0
buzzerTimer = 3
buzzerChannel = 3

# LED constants
LEDpin = pyb.Pin.board.PB4
LEDtimer = 3
LEDchannel = 1


# initialize motors, encoders, LED, alarm objects
motor1 = MotorDriver2(motor1Pin1, motor1Pin2, motor1Ena, motor1Tim, motor1Ch1)
motor2 = MotorDriver2(motor2Pin1, motor2Pin2, motor2Ena, motor2Tim, motor2Ch1)
encoder1 = EncoderReader(encoder1Pin1, encoder1Pin2, encoder1Tim, encoder1Ch1, encoder1Ch2)
encoder2 = EncoderReader(encoder2Pin1, encoder2Pin2, encoder2Tim, encoder2Ch1, encoder2Ch2)
LED = FireLED(LEDpin, LEDtimer, LEDchannel)
alarm = Buzzer(buzzerPin, buzzerTimer, buzzerChannel)

#MLX_CAM stuff

def loop():
    try:
        from pyb import info

    # Oops, it's not an STM32; assume generic machine.I2C for ESP32 and others
    except ImportError:
        # For ESP32 38-pin cheapo board from NodeMCU, KeeYees, etc.
        i2c_bus = I2C(1, scl=Pin(22), sda=Pin(21))

    # OK, we do have an STM32, so just use the default pin assignments for I2C1
    else:
        i2c_bus = I2C(1)

#     print("MXL90640 Easy(ish) Driver Test")

    # Select MLX90640 camera I2C address, normally 0x33, and check the bus
    i2c_address = 0x33
    scanhex = [f"0x{addr:X}" for addr in i2c_bus.scan()]
#     print(f"I2C Scan: {scanhex}")
#     print(gc.mem_free())
    gc.collect()
#     print(gc.mem_free())
    camera = MLX_Cam(i2c_bus)
    
    gc.collect()
#     print(gc.mem_free())
    
#     image = camera.get_image()

    KP1 = .15
    KP2 = .15
    
    while True:
        #gc.collect()
        image = camera.get_image()
        #gc.collect()
        camera.ascii_art(image)
#         print(camera.target_alg())
        
        Yaw_error, Pitch_error = camera.target_alg([6, 22])
        
        setPoint1 = Yaw_error*61
        setPoint2 = Pitch_error*61
        control1 = Control(KP1, setPoint1 + 32768)
        control2 = Control(KP1, setPoint2 + 32768)
        
        #print(f'{setPoint1}')
        #print(f'{setPoint2}')
        psi1 = 101
        encoder1.zero()
        encoder2.zero()
        elapsed = 0
        startTime = time.ticks_ms()
#         while (psi1 > 10):
        while(elapsed<500):
            elapsed = time.ticks_ms() - startTime
            pos1 = encoder1.read()
            pos2 = encoder2.read()
            #print(pos1)
            psi1 = control1.run(pos1)
            alarm.beep(psi1)
            motor1.set_duty_cycle(-psi1)
            pyb.delay(5)
            
            psi2 = control2.run(pos2)
            motor2.set_duty_cycle(-psi2)
            #print(psi)
            pyb.delay(5)
            
            #print(psi1, psi2)
        
#         print("done")
        motor1.set_duty_cycle(0)
        motor2.set_duty_cycle(0)
        
def checkCont(yaw, pitch):
    KP1 = .15
    KP2 = .15
    setPoint1 = yaw*61
    setPoint2 = pitch*61
    control1 = Control(KP1, setPoint1 + 32768)
    control2 = Control(KP1, setPoint2 + 32768)
    
    #print(f'{setPoint1}')
    #print(f'{setPoint2}')
    psi1 = 101
    encoder1.zero()
    encoder2.zero()
    elapsed = 0
    startTime = time.ticks_ms()
#         while (psi1 > 10):
    while(elapsed<500):
        elapsed = time.ticks_ms() - startTime
        pos1 = encoder1.read()
        pos2 = encoder2.read()
        #print(pos1)
        psi1 = control1.run(pos1)
        motor1.set_duty_cycle(-psi1)
        pyb.delay(5)
        
        psi2 = control2.run(pos2)
        motor2.set_duty_cycle(-psi2)
        #print(psi)
        pyb.delay(5)
        
        #print(psi1, psi2)
    
    print("done")
    motor1.set_duty_cycle(0)
    motor2.set_duty_cycle(0)
    
if __name__ == "__main__":
    while True:
        print("Down")
        pyb.delay(500)
        checkCont(4,4)
        pyb.delay(500)
        print("Up")
        pyb.delay(500)
        checkCont(-4,-4)
        pyb.delay(500)
    