"""!
@file duelmainfile.py

This file is for ME 405's final project demonstration, in which two competing teams carry out a duel between
heat-seaking Nerf turrets. The goal of a duel is to be the first to hit an opposing target, without missing a shot (penalty).
A heat-seaking nerf turret uses an MLX90640 infrared camera to find a target based off its heat signature, two motors to control
the yaw and pitch of the turret, two constantly-spinning flywheel motors to launch the darts, a servo to actuate the firing pin,
and a set of LED's and a beeper for human interaction.

**Yaw-Axis:** The yaw axis is controlled by a 50:1 metal, geared-down, encoded, 24V DC brushed motor with a maximum RPM
of 200. This motor uses a timing pulley system at a 4:1 gear ratio to control the lateral aim of the turret. A Kyuionty L298
DC Motor Driver is used to control the motor through pulse-width modification. The yaw motor is initialized as an object of
class MotorDriver2 and controlled using PID control in class Control2 to act as a servo.

<b>Pitch-Axis:</b> The pitch axis is configured similarly to the yaw-axis. It is controlled by a 50:1 metal, geared-down, encoded,
24V DC brushed motor with a macimum RPM of 200. The motor uses a pulley timing system with a 4:1 gear ratio to control the
vertical aim of the turret. The pitch motor is initialized as an object of class MotorDriver2 and controlled using PID control
to act as a servo.

<b>Motor Control:</b> Both the yaw and pitch motors are controled using PID control to act as positional servos. PID control stands
for proportional, integral, and derivataive control, and is used to modify the response of a motor. Proportional control is the
simplest form of motor control. It calculates the system error ("goal" encoder value - actual encoder value) and multiplies it
by a constant, Kp, to modify how much effort the motor applies to reach its goal. Integral control is used to modify the steady-state
condition of the motor and to eliminate steady state error. It involves continuously summing the error and dividing it by the change
in time, and using that value to adjust the control inputs. As time goes on, the effect of integral control increases. Derivative
control uses the rate of change of the error to adjust the system's control inputs. It is best used to control the transient
response of a system, which is when the error's rate of change is the highest. Using PID control allows the turret to respond more
quickly and accurately, imrpoving the aim and speed of the system.

<b>Flywheels:</b> The flywheel motors are 24V DC Brushed Motors with a maximum rpm of 20000 at 24V. They are controlled with PWM by a
motor driver which sends the same signal to both motors (in opposite direction). The flywheels have a radius of 2.5 inches, meaning
the velocity at the contact point between the Nerf Dart and the flywheel is equal tot he angular velocity (in radians/sec) * 3.
Therefore, at its maximum rpm of 12000, the contact point velocity would be ~ 440 fps [feet per sercond]. In order to operate the
turret under safe conditions, the flywheelse idle at a duty cycle of 5% and ramp up to 10% to fire at a safe velocity.

<b>Servo:</b> A metal-geared high-torque DC servo is used to control the actuation of the firing pin. Controlling a DC servo is
different than controlling a DC motor to act as a servo because the DC servo is already configured to be positionally controlled.
PWM duty cycles are sent through the servo's signal wire to control the position of the servo.

<b>Buzzer/LED's:</b> A buzzer is used to allow for better human-turret interaction. Different beep sequences are used to communicate
when the turret is waiting for a pushbutton input, when it has received that input, and which mode it is in. LED's are also mounted
on the barrel of the turret to communicate in a similar manner.

<b>MLX90640 IR Camera:</b> An MLX90640 Infrared Camera is mounted to the barrel of the turret, and is used to locate a target and
return setpoints for the yaw and pitch motors. When the camera takes an image, it returns a 24 x 32 array of values, corresponding
to heat signature. Dr. Ridgley provided the mlx_cam driver with functionality to configure the camera via I2C, capture an image, and
scale/process the data into a pixel map, an ascii art image, and a csv data file. The camera takes ~400-600 ms to capture an image.
Once the image is captured, the data is scaled, and then a target can be found. In general, humans have a higher heat signature than
their surroundings in a classroom.

<b>Targeting & Aiming:</b> The targeting algorithm can be found in the file mlx_cam.py in the mlx_raw folder of the directory. The main
strategy applied in that algorithm favors targets with a vertical aspect ratio (humans are generally taller than they are wide). The
strategy is as follows:
    1. Index through the searchable columns of the 2D pixel array. In each column, sum the square of the pixel value of any pixel that
    is above a pre-defined threshold. The column with the greatest sum is set as the horizontal position of the target. Having the
    threshold value and squaring each pixel value before they are added to the sum means that warmer pixels have a higher weight,
    meaning a column with a few "very hot" pixels will likely have a larger sum than one with many warm pixels. This locates the
    horizontal center of the person.
    
    2. In the column with the highest sum, search for the pixel with the highest value. Multiple pixels on the target in that column
    may have the same maximum value. The search is conducted vertically (top to bottom), so each pixel value that matches the hottest
    value overwrites the old one. In general, this will aim for the vertical center of the target.
    
    *Note: Only columns 6 --> 26 and rows 4 --> 15 are searched. When looking for a target, the turret is aimed down the center of the
    duel table. Removing the outer pixels from the search causes the turret to only search for a target in the pre-defined area that a
    target is allowed to stand.



<b>Duel Proceedings:</b> Before running DuelMainFile.py, **ensure that motor power is switched off** and that the turret is spun around,
facing the opposite direction of the target. Once the code has begun and all pins have been initialized, the user is prompted to push
the pushbutton to run the turret's "wakeUp()" function in which it commences shakedown. Ensure that all motors and the servo actuated
and returned to their previous position. The turret is now ready to begin a duel.

At the "start" signal from the duel operator, the push button must be compressed to begin the turret's duel cycle. The turret will spin
180 degrees counterclockwise to face the target. During the first 5 seconds of the duel, the targets are allowed to move. Due to the
limitations of the camera and driver provided, it takes roughly 650-850 ms to capture an image, find the target, and aim the turret at it.
This rate is too slow to actively track and shoot a moving target, so the turret sits in idle. After the 5 second period is over and the
targets have been instructed to "freeze", the turret captures an image and finds the target (400-600 ms), aims towards the position
provided by the targeting algorithm (250 ms), and fires.

Once the turret has fired, it enters "sleep" mode by decreasing the idle speed of the flywheels and returning to its home position (facing
away from the target). From that point, the pushbutton may be engaged again at the beginning of the duel.

A note on code structure: Our team elected to not use multitasking to conduct the duel. Since the order of proceedings was fairly preset
(turn 180 --> wait 5 seconds --> get image --> find target --> aim --> shoot), electing to not use multitasking allowed for direct
modificaiton of the exact activity of the turret during a duel at any point in time.


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

