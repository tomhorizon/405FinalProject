import pyb
import utime

class Servo:
    """! @brief Servo class is used to control a servo using PWM positioning
    """
    def __init__(self, pin1, tim_num, chan_num):
        """! The initialization sets the attributes for a servo object including its signal pin, initialized position, and
        timing attributes. The servo is used to control the linear motion of a firing pin. The servo is initialized in the
        position to bring the turret's firing pin fully back (disengaged). A PWM value of 23000 puts the firing pin in its
        disengaged position, and PWM = 18000 engages the firing pin
        
        @param pin1: PYB pin that the servo signal pin is connected to
        @param tim_num: Timer number used to control the servo
        @param chan_num: Timer channel number used to control the servo
        """
        servo_signal = pyb.Timer(tim_num, freq=250)
        servo_pin = pyb.Pin(pin1, pyb.Pin.OUT_PP)
        self.signal_ch = servo_signal.channel(chan_num, pyb.Timer.PWM, pin=servo_pin, pulse_width=23000)
        
    def powerUp(self):
        """! The powerUp() method is used during the turret's wakeUp phase. It partially actuates the firing pin once and is
        used to visually confirm proper servo function and positioning.
        """
        print("servo disengage")
        self.signal_ch.pulse_width(23000)
        pyb.delay(270)
        self.signal_ch.pulse_width(18000)
        pyb.delay(100)
        self.signal_ch.pulse_width(23000)
        pyb.delay(100)
        
    def fire(self):
        """! The fire() method is used to fully engage and then disengage the firing pin once, causing the turret to fire one shot.
        """
        print("servo engage")
        self.signal_ch.pulse_width(8000)
        pyb.delay(270)
        print("servo disengage")
        self.signal_ch.pulse_width(23000)
        pyb.delay(270)
    
    def magDump(self, num):
        """! The magDump() method is used to fully engage and then disengage the firing pin multiple times, causing the turret to
        fire a specified number of darts.
        @param num: Number of shots to be fired
        """
        for i in range(num):
            self.signal_ch.pulse_width(8000)
            pyb.delay(300)
            self.signal_ch.pulse_width(23000)
            pyb.delay(400)
        
if __name__ == '__main__':
    # Servo test code used to fully engage and disengage the firing pin repeatedly    
    
    while 0:
        print("Servo Engage")
        signal_ch.pulse_width(8000)
        pyb.delay(250)
        print("Servo Disengage")
        signal_ch.pulse_width(23000)
        pyb.delay(250)
        print("shot")
    
    while 1:
        serv = Servo(pyb.Pin.board.PC9, 3, 4)
        #serv.fire()
        print("start")
        serv.magDump(3)
        print("done")
        pyb.delay(2000)
    
    

