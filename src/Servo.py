import pyb
import utime

class Servo:

    def __init__(self, pin1, tim_num, chan_num):
        servo_signal = pyb.Timer(tim_num, freq=250)
        servo_pin = pyb.Pin(pin1, pyb.Pin.OUT_PP)
        self.signal_ch = servo_signal.channel(chan_num, pyb.Timer.PWM, pin=servo_pin, pulse_width=23000)
        self.forward = 8000
        self.back = 23000
        self.time = 350
        
        
    def fire(self):
        print("servo engage")
        self.signal_ch.pulse_width(8000)
        pyb.delay(270)
        print("servo disengage")
        self.signal_ch.pulse_width(23000)
        pyb.delay(270)
    
    def magDump(self, num):
        for i in range(num):
            self.signal_ch.pulse_width(8000)
            pyb.delay(270)
            self.signal_ch.pulse_width(23000)
            pyb.delay(270)
        
if __name__ == '__main__':
    
    #servo_signal = pyb.Timer(3, freq=250)
    #servo_pin = pyb.Pin(pyb.Pin.board.PC9, pyb.Pin.OUT_PP)
    #signal_ch = servo_signal.channel(4, pyb.Timer.PWM, pin=servo_pin, pulse_width=23000)
    
    
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
        serv.fire()
    
    

