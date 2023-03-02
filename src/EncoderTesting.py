import pyb
import utime
from motor_driver import MotorDriver
from encoder_reader import EncoderReader
from control import Control
from mlx_cam import MLX_Cam
from machine import Pin, I2C

# motor constants
motor1Pin1 = pyb.Pin.board.PB4
motor1Pin2 = pyb.Pin.board.PB5
motor1Ena = pyb.Pin.board.PA10
motor1Tim = 3
motor1Ch1 = 1
motor1Ch2 = 2

# motor2Pin1 = pyb.Pin.board.PA0
# motor2Pin2 = pyb.Pin.board.PA1
# motor2Ena = pyb.Pin.board.PC1
# motor2Tim = 5
# motor2Ch1 = 1
# motor2Ch2 = 2

# encoder constants
encoder1Pin1 = pyb.Pin.board.PB6
encoder1Pin2 = pyb.Pin.board.PB7
encoder1Tim = 4
encoder1Ch1 = 1
encoder1Ch2 = 2
# encoder2Pin1 = pyb.Pin.board.PC6
# encoder2Pin2 = pyb.Pin.board.PC7
# encoder2Tim = 8
# encoder2Ch1 = 1
# encoder2Ch2 = 2

# initialize motors and encoder objects
motor1 = MotorDriver(motor1Ena, motor1Pin1, motor1Pin2, motor1Tim, motor1Ch1, motor1Ch2)
# motor2 = MotorDriver(motor2Ena, motor2Pin1, motor2Pin2, motor2Tim, motor2Ch1, motor2Ch2)
encoder1 = EncoderReader(encoder1Pin1, encoder1Pin2, encoder1Tim, encoder1Ch1, encoder1Ch2)
# encoder2 = EncoderReader(encoder2Pin1, encoder2Pin2, encoder2Tim, encoder2Ch1, encoder2Ch2)

def main():
    
    KP1 = .1
            
    setPoint1 = 5000
    
    control1 = Control(KP1, setPoint1 + 32768)
    
    print(f'{setPoint1}, {KP1}')
    encoder1.zero()
    elapsed = 0
    startTime = utime.ticks_ms()
    count = 0
    while elapsed <= 3000:
        currentTime = utime.ticks_ms()
        elapsed = currentTime - startTime

        pos1 = encoder1.read()
        print(pos1)
        psi = control1.run(pos1)
        motor1.set_duty_cycle(-psi)
        #print(psi)
        pyb.delay(10)
        count += 1
    
    print("done")
    motor1.set_duty_cycle(0)
    #motor2.set_duty_cycle(0)
    
    
    KP1 = .1
    setPoint1 = -5000
    
    control1 = Control(KP1, setPoint1 + 32768)
    print(f'{setPoint1}, {KP1}')
    encoder1.zero()
    elapsed = 0
    startTime = utime.ticks_ms()
    count = 0
    while elapsed <= 3000:
        currentTime = utime.ticks_ms()
        elapsed = currentTime - startTime

        pos1 = encoder1.read()
        print(pos1)
        psi = control1.run(pos1)
        motor1.set_duty_cycle(-psi)
        #print(psi)
        pyb.delay(10)
        count += 1
    
    print("done")
    motor1.set_duty_cycle(0)
    
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

    print("MXL90640 Easy(ish) Driver Test")

    # Select MLX90640 camera I2C address, normally 0x33, and check the bus
    i2c_address = 0x33
    scanhex = [f"0x{addr:X}" for addr in i2c_bus.scan()]
    print(f"I2C Scan: {scanhex}")
    camera = MLX_Cam(i2c_bus)
    
    KP1 = .1
    
    while True:
        camera.ascii_art(image.v_ir)
        print(camera.target_alg())
        
        Yaw_error, Pitch_error = target_alg()
        
        setPoint1 = Yaw_error*5
        control1 = Control(KP1, setPoint1 + 32768)
        
        print(f'{setPoint1}, {KP1}')
        encoder1.zero()
        elapsed = 0
        startTime = utime.ticks_ms()
        while elapsed <= 1000:
            currentTime = utime.ticks_ms()
            elapsed = currentTime - startTime

            pos1 = encoder1.read()
            #print(pos1)
            psi = control1.run(pos1)
            motor1.set_duty_cycle(-psi)
            #print(psi)
            pyb.delay(10)
        
        print("done")
        motor1.set_duty_cycle(0)
        #motor2.set_duty_cycle(0)
    
    
if __name__ == "__main__":
    loop()
    pyb.delay(10)