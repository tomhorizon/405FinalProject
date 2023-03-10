import pyb
import utime

class Flywheel():
    def __init__(self):
        motorTimer = pyb.Timer(3, freq=50)
        motorpin1 = pyb.Pin(pyb.Pin.board.PC0, pyb.Pin.OUT_PP)
        motorpin2 = pyb.Pin(pyb.Pin.board.PC3, pyb.Pin.OUT_PP)
        enablepin = pyb.Pin(pyb.Pin.board.PC8, pyb.Pin.OUT_PP)flfl
        motorch1 = motorTimer.channel(3, pyb.Timer.PWM, pin=enablepin)
        motorch1.pulse_width_percent(0)
        motorpin1.value(0)
        motorpin2.value(0)
        
    def murder(self, level):
        if level == 0:
            motorpin1.value(0)
            motorpin2.value(0)
        else:
            motorch1.pulse_width_percent(int(level))
            motorpin1.value(0)
            motorpin2.value(1)
            

    
        

