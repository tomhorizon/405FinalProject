"""!
@file lab3main.py

This file is for ME 405's final project demonstration, in which two competing teams carry out a duel between
heat-seaking Nerf turrets. A heat-seaking nerf turret uses an MLX90640 infrared camera to find a target based
off its heat signature, two motors to control the yaw and pitch of the turret, two constantly-spinning flywheel
motors to launch the darts, a servo to actuate the firing pin, and a set of LED's and a beeper for human interaction.

<b>Yaw-Axis:<b> The yaw axis is controlled by a 50:1 metal, geared-down, encoded, 24V DC brushed motor with a maximum RPM
of 200. This motor uses a timing pulley system at a 4:1 gear ratio to control the lateral aim of the turret. A Kyuionty L298
DC Motor Driver is used to control the motor through pulse-width modification. The yaw motor is initialized as an object of
class MotorDriver2 and controlled using PID control in class Control2 to act as a servo.

<b>Pitch-Axis:<b> The pitch axis is configured similarly to the yaw-axis. It is controlled by a 50:1 metal, geared-down, encoded,
24V DC brushed motor with a macimum RPM of 200. The motor uses a pulley timing system with a 4:1 gear ratio to control the
vertical aim of the turret. The pitch motor is initialized as an object of class MotorDriver2 and controlled using PID control
to act as a servo.

<b>Motor Control:<b> Both the yaw and pitch motors are controled using PID control to act as positional servos. PID control stands
for proportional, integral, and derivataive control, and is used to modify the response of a motor. Proportional control is the
simplest form of motor control. It calculates the system error ("goal" encoder value - actual encoder value) and multiplies it
by a constant, Kp, to modify how much effort the motor applies to reach its goal. Integral control is used to modify the steady-state
condition of the motor and to eliminate steady state error. It involves continuously summing the error and dividing it by the change
in time, and using that value to adjust the control inputs. As time goes on, the effect of integral control increases. Derivative
control uses the rate of change of the error to adjust the system's control inputs. It is best used to control the transient
response of a system, which is when the error's rate of change is the highest. Using PID control allows the turret to respond more
quickly and accurately, imrpoving the aim and speed of the system.

<b>Flywheels:<b>

<b>Servo:<b>

<b>Buzzer/LED's:<b>

<b>MLX90640 IR Camera:<b>

<b>Duel Proceedings:<b>


@author Tom Taylor
@author Jonathan Fraser
@author Dylan Weiglein

@date   2023-3-16
"""
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

