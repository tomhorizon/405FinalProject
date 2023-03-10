import pyb
import utime

class Flywheel():
    def __init__(self):
        motorTimer = pyb.Timer(3, freq=50)
        self.motorpin1 = pyb.Pin(pyb.Pin.board.PC0, pyb.Pin.OUT_PP)
        self.motorpin2 = pyb.Pin(pyb.Pin.board.PC3, pyb.Pin.OUT_PP)
        enablepin = pyb.Pin(pyb.Pin.board.PC8, pyb.Pin.OUT_PP)
        self.motorch1 = motorTimer.channel(3, pyb.Timer.PWM, pin=enablepin)
        self.motorch1.pulse_width_percent(0)
        self.motorpin1.value(0)
        self.motorpin2.value(1)
        
    def murder(self, level):
#         if level == 0:
#             self.motorpin1.value(0)
#             self.motorpin2.value(0)
#        else:
        self.motorch1.pulse_width_percent(int(level))
        self.motorpin1.value(0)
        self.motorpin2.value(1)
            
if __name__ == "__main__":
    flywheel = Flywheel()
    while True:
        print("on")
        for i in range (250):
            flywheel.murder(i/10)
            pyb.delay(100)
            print(i/50)
        flywheel.murder(0)
        print("off")
        pyb.delay(2000)
        
        
        

