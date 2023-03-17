import pyb
from control2 import Control2
import utime as time

class Turret:
    """! @brief Turret class creates and carries out all of the functios of a heat-seekign nerf turret.
    """
    def __init__(self, yawMotor, pitchMotor, yawEncoder, pitchEncoder, flywheel, servo, LED, alarm, camera, goButton):
        """! The initialization sets the attributes for a turret object
        @param yawMotor: Motor that controls the yaw axis, object of MotorDriver2 class
        @param pitchMotor: Motor that controls the pitch axis, object of MotorDriver2 class
        @param yawEncoder: The turret uses an encoder from class EncoderDriver to read yaw position
        @param pitchEncoder: The turret uses an encoder from class pitchEncoder to read pitch position
        @param flywheel: The turret uses flywheels from class MotorDriver 2 to propel darts
        @param servo: The turret uses a servo to control the firing pin from class Servo
        @param LED: The turret uses LED's to communicate psi values and turret mode
        @param alarm: The turret uses an alarm to communicate with user and to communicate activity
        @param camera: The turret uses an IR camera of class MLX_Cam to find a target
        @param goButton: The turret uses a limit switch as the main source of user input
        """

        self.yawMotor = yawMotor
        self.pitchMotor = pitchMotor
        self.yawEncoder = yawEncoder
        self.pitchEncoder = pitchEncoder
        self.flywheel = flywheel
        self.servo = servo
        self.LED = LED
        self.alarm = alarm
        self.camera = camera
        self.goButton = goButton
        self.track_yaw = 0
        self.flywheel.set_duty_cycle(0)
        
        self.KP1 = .009
        self.KI1 = .021
        self.KD1 = .01

        self.KP2 = .008
        self.KI2 = .015
        self.KD2 = .03
        
    def wakeUp(self):
        """! The turret powers on, checks for safety, and actuates each motor (shakedown) to ensure proper function
        """
        print("Booting up...")
        self.yawEncoder.zero()
        self.pitchEncoder.zero()
        
#         self.alarm.powerUp()
        self.LED.powerUp()
        
        print("Enter to start shakedown. Turn on High Voltage Power before continuing.\nEnsure turret is level and safe to rotate.")
        self.alarm.numBeep(1)
        while self.goButton.value() == 0:
            pyb.delay(3)
        self.alarm.numBeep(2)
        
        self.servo.powerUp()
        self.flywheel.set_duty_cycle(0)
        self.flywheel.set_duty_cycle(3)
        pyb.delay(500)
        self.flywheel.set_duty_cycle(0)
        
        self.yawMotor.set_duty_cycle(-35)
        pyb.delay(200)
        self.yawMotor.set_duty_cycle(35)
        pyb.delay(200)
        self.yawMotor.set_duty_cycle(0)
        pyb.delay(100)
        
        self.pitchMotor.set_duty_cycle(-25)
        pyb.delay(150)
        self.pitchMotor.set_duty_cycle(25)
        pyb.delay(100)
        self.pitchMotor.set_duty_cycle(0)
        pyb.delay(100)
        
        print("Shakedown complete.")
        self.flywheel.set_duty_cycle(5)
    
    def yaw180(self):
        """! The turret rotates 180 degrees clockwise around its yaw axis
        """
        self.track_yaw = 0
        self.yawEncoder.zero()
        self.pitchEncoder.zero()
        #change pain level here  (x / 100)
        #fire up flywheel
        self.flywheel.set_duty_cycle(12)
        
        self.LED.hunt()
        
        # rotate 180 - seems to be around 7000
        # positive yaw: CCW
        # positive pitch: DOWN
        setPoint1 = 6400 # just testing on my desk an don't want it rotating lol
        setPoint2 = 0
        self.track_yaw = self.track_yaw + setPoint1
        psi1 = 101
        control1 = Control2(self.KP1, self.KI1, self.KD1, setPoint1 + 32768)
        pyb.delay(5)
        elapsed = 0
        start = time.ticks_ms()
        while (elapsed < 1500):
            elapsed = time.ticks_ms() - start
            pos1 = self.yawEncoder.read()
            psi1 = control1.run(pos1)
            self.yawMotor.set_duty_cycle(-psi1)
            pyb.delay(5)
#             print(psi1)
            #psi1 = 0
            
        self.yawMotor.set_duty_cycle(0)
        self.pitchMotor.set_duty_cycle(0)
        
    def findTarget(self, xrange):
        """! The turret uses the camera to capture an image and find a target to be aimed at
        @param xrange: contains the minimum and maximum indexes of columns to search (can range from 1 --> 31)
        """
        image = self.camera.get_image()
        self.camera.ascii_art(image)
        self.yawError, self.pitchError = self.camera.target_alg(xrange)
    
    def aim(self):
        """! The turret uses the yaw and pitch errors and their respective motors to aim at the selected target
        """
        setPoint1 = self.yawError*61
        if self.yawError >= 0:
            setPoint1 = setPoint1 - 150
        else:
            setPoint1 = setPoint1 + 150
        setPoint2 = self.pitchError*61
        
        self.track_yaw = self.track_yaw + setPoint1

        print(f"Yaw_e = {self.yawError}, Pitch_e = {self.pitchError}")
        self.yawEncoder.zero()
        self.pitchEncoder.zero()
        
        elapsed = 0
        psi1 = 101
        control1 = Control2(self.KP1, self.KI1, self.KD1, setPoint1 + 32768)
        control2 = Control2(self.KP2, self.KI2, self.KD2, setPoint2 + 32768)
        pyb.delay(5)
        start = time.ticks_ms()
        while (elapsed < 250):
            elapsed = time.ticks_ms() - start
            pos1 = self.yawEncoder.read()
            pos2 = self.pitchEncoder.read()
            
            psi1 = control1.run(pos1)
            psi2 = control2.run(pos2)
            
            self.yawMotor.set_duty_cycle(-psi1)
            self.pitchMotor.set_duty_cycle(psi2)
            
            self.alarm.beep(abs(psi1))
            pyb.delay(5)
#             print(psi1)
            #psi1 = 0
            
        self.yawMotor.set_duty_cycle(0)
        self.pitchMotor.set_duty_cycle(0)
        
    def fire(self, n):
        """! The turret fires a specified number of rounds at the target
        @param n: number of rounds to be fired
        """
        self.servo.magDump(n)
        self.LED.on()
        self.alarm.off()
        self.flywheel.set_duty_cycle(3)
        print("Target Engaged")
        
    def sleep(self):
        """! The turret resets to its home position and lowers flywheel duty cycle to a safer speed
        """
        self.yawEncoder.zero()
        self.pitchEncoder.zero()
        
        self.flywheel.set_duty_cycle(5)
        
        control1 = Control2(self.KP1, self.KI1, self.KD1, -self.track_yaw + 32768)
        pyb.delay(5)
        elapsed = 0
        start = time.ticks_ms()
        while (elapsed < 1500):
            elapsed = time.ticks_ms() - start
            pos1 = self.yawEncoder.read()
            psi1 = control1.run(pos1)
            self.yawMotor.set_duty_cycle(-psi1)
            pyb.delay(5)
#             print(psi1)
            #psi1 = 0
            
        self.yawMotor.set_duty_cycle(0)
        self.pitchMotor.set_duty_cycle(0)
        
        
