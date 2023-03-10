import pyb
import utime

class Servo:

    def __init__(self, pin1, tim_num, chan_num):
        self.servo_signal = pyb.Timer(tim_num, freq=250)
        self.servo_pin = pyb.Pin(pin1, pyb.Pin.OUT_PP)
        self.signal_ch = self.servo_signal.channel(chan_num, pyb.Timer.PWM, pin=self.servo_pin, pulse_width=19000)
            
        
        
    def fire(self):
        self.signal_ch.pulse_width(8000)
        pyb.delay(400)
        self.signal_ch.pulse_width(19000)
        pyb.delay(400)
        
if __name__ == '__main__':
    servo_signal = pyb.Timer(3, freq=250)
    servo_pin = pyb.Pin(pyb.Pin.board.PC9, pyb.Pin.OUT_PP)
    signal_ch = servo_signal.channel(4, pyb.Timer.PWM, pin=servo_pin, pulse_width=8000)
    while True:
        signal_ch.pulse_width(8000)
        pyb.delay(400)
        signal_ch.pulse_width(19000)
        pyb.delay(400)
        print("shot")
    
    

