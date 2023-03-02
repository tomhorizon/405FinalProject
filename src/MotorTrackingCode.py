"""!
@file lab3main.py

This file is Lab 3 for ME 405. The goal of this exercise was to simultaneously control two 12V
DC motor system as individual servos with proportional controllers using a real-time scheduler.
The scheduler allows us to use multitasking by scheduling the sequence in which tasks are carried
out in correspondance to the preset frequency.

The motors are connected to an external power supply and a STM32 PWM output. The built-in encoder
provides position feedback and uses STM-32 timers. At the beginning of the
program sequence, controller parameters are sent through UART serial communication
to the STM32, initializing the control algorithm.

The proportional controller is the most simple closed-loop controller, using
just one variable (Kp, the controller constant), to direcetly impact the amount
of "effort" that the motor applies. The "effort" applied to the motor is a duty
cycle percentage. To find the required duty cycle, the algorithm calculates the
difference between the setpoint (goal) and the actual position and multiplies it
by the proportional controller constant. A higher error implies a higher corrective
effort, while a lower error applied a lower corrective effort. Eventually, the
error becomes negligible and no further correction is needed.

This program uses 3 classes: MotorDriver, EncoderReader, and Control. After defining
the pins and starting the timer channels, the control loop waits for motor parameters.
Once the controller parameters (Kp and setpt) are received from the PC. The encoder
reads the position, which is used by the controller to calculate the required duty
cycle, which is applied to the motor. This loop runs for 3 seconds.

Dr. Ridgley's cotask class and functions are used to implement multitasking. This allowed us to
accomplish the above tasks on two motors simultaneously.

@author Tom Taylor
@author Jonathan Fraser
@author Dylan Weiglein

@date   2022-02-15
"""
import pyb
import utime
from motor_driver import MotorDriver
from encoder_reader import EncoderReader
from control import Control
import cotask
import task_share

from machine import Pin, I2C
from mlx90640 import MLX90640
from mlx90640 import RefreshRate
from mlx90640.calibration import NUM_ROWS, NUM_COLS, IMAGE_SIZE, TEMP_K
from mlx90640.image import ChessPattern, InterleavedPattern
from mlx_cam import MLX_Cam


KP1 = 0.2 # yaw
KP2 = 0.2 # pitch
runtime = 5000 #ms

# initialize motors and encoder objects

def motor1task(shares):  #Yaw
    
    # motor constants
    motor1Pin1 = pyb.Pin.board.PB4
    motor1Pin2 = pyb.Pin.board.PB5
    motor1Ena = pyb.Pin.board.PA10
    motor1Tim = 3
    motor1Ch1 = 1
    motor1Ch2 = 2
    
    # encoder constants
    encoder1Pin1 = pyb.Pin.board.PB6
    encoder1Pin2 = pyb.Pin.board.PB7
    encoder1Tim = 4
    encoder1Ch1 = 1
    encoder1Ch2 = 2
    
    kp, setpoint, = shares
    
    motor1 = MotorDriver(motor1Ena, motor1Pin1, motor1Pin2, motor1Tim, motor1Ch1, motor1Ch2)
    encoder1 = EncoderReader(encoder1Pin1, encoder1Pin2, encoder1Tim, encoder1Ch1, encoder1Ch2)
    control1 = Control(kp.get(), setpoint.get())
    
    encoder1.zero()
    while True:
        pos1 = encoder1.read()
        psi = control1.run(pos1)
        motor1.set_duty_cycle(psi)
        yield 0

def motor2task(shares): #pitch motor
    
    # motor constants
    motor2Pin1 = pyb.Pin.board.PA0
    motor2Pin2 = pyb.Pin.board.PA1
    motor2Ena = pyb.Pin.board.PC1
    motor2Tim = 5
    motor2Ch1 = 1
    motor2Ch2 = 2
    
    # encoder constants
    encoder2Pin1 = pyb.Pin.board.PC6
    encoder2Pin2 = pyb.Pin.board.PC7
    encoder2Tim = 8
    encoder2Ch1 = 1
    encoder2Ch2 = 2
    
    kp, setpoint = shares
    motor2 = MotorDriver(motor2Ena, motor2Pin1, motor2Pin2, motor2Tim, motor2Ch1, motor2Ch2)
    encoder2 = EncoderReader(encoder2Pin1, encoder2Pin2, encoder2Tim, encoder2Ch1, encoder2Ch2)
    
    control2 = Control(kp.get(), setpoint.get())
    encoder2.zero()
    while True:
        pos2 = encoder2.read()
        psi = control2.run(pos2)
        motor2.set_duty_cycle(psi)
        yield 0
        
def cameratask(shares):
    #initialize camera
    YawError, PitchError = shares
    # The following import is only used to check if we have an STM32 board such
    # as a Pyboard or Nucleo; if not, use a different library
    try:
        from pyb import info

    # Oops, it's not an STM32; assume generic machine.I2C for ESP32 and others
    except ImportError:
        # For ESP32 38-pin cheapo board from NodeMCU, KeeYees, etc.
        i2c_bus = I2C(1, scl=Pin(22), sda=Pin(21))

    # OK, we do have an STM32, so just use the default pin assignments for I2C1
    else:
        i2c_bus = I2C(1)

    # Select MLX90640 camera I2C address, normally 0x33, and check the bus
    i2c_address = 0x33
    scanhex = [f"0x{addr:X}" for addr in i2c_bus.scan()]
    print(f"I2C Scan: {scanhex}")
    
    camera = MLX_Cam(i2c_bus)
    
    while True:
        # take image
        # x, y = calculate yaw, pitch error in pixels
        try:
            # Get and image and see how long it takes to grab that image
            print("Click.", end='')
            begintime = time.ticks_ms()
            image = camera.get_image()
            print(f" {time.ticks_diff(time.ticks_ms(), begintime)} ms")

            # Can show image.v_ir, image.alpha, or image.buf; image.v_ir best?
            # Display pixellated grayscale or numbers in CSV format; the CSV
            # could also be written to a file. Spreadsheets, Matlab(tm), or
            # CPython can read CSV and make a decent false-color heat plot.
            show_image = False
            show_csv = False
            if show_image:
                camera.ascii_image(image.v_ir)
            elif show_csv:
                for line in camera.get_csv(image.v_ir, limits=(0, 99)):
                    print(line)
            #else:
            camera.ascii_art(image.v_ir)
            x,y = camera.target_alg()
            print(camera.target_alg())
            
        except KeyboardInterrupt:
            break
        YawError.put(x)
        PitchError.put(y)
        yield 0
    


def main():
    # Create a share and a queue to test function and diagnostic printouts
    KP1share = task_share.Share('f', thread_protect=False, name="KP 1")
    SP1share = task_share.Share('h', thread_protect=False, name="Setpoint 1")
    KP2share = task_share.Share('f', thread_protect=False, name="KP 2")
    SP2share = task_share.Share('h', thread_protect=False, name="Setpoint 2")
    YawShare = task_share.Share('b', thread_protect=False, name="Yaw Error")
    PitchShare = task_share.Share('b', thread_protect=False, name="Pitch Error")


    task_1 = cotask.Task (cameratask, name = "Camera Task",
                          priority = 1, period = 100, profile = True, trace=False, shares=(YawShare, PitchShare))
    task_2 = cotask.Task (motor1task, name = "Control Motor 1",
                          priority = 2, period = 10, profile = True, trace=False, shares=(KP1share, YawShare))
    task_3 = cotask.Task (motor2task, name = "Control Motor 2",
                          priority = 2, period = 10, profile = True, trace=False, shares=(KP2share, PitchShare))

    cotask.task_list.append (task_1)
    cotask.task_list.append (task_2)
    cotask.task_list.append (task_3)
    
    KP1share.put(KP1)
    SP1share.put(0)
    KP2share.put(KP2)
    SP2share.put(0)

    while 1:
        cotask.task_list.pri_sched ()
    
    
if __name__ == "__main__":
    while True:
        main()

