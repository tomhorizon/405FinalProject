import pyb
import utime


servo_signal = pyb.Timer(4, freq=250)
servo_pin = pyb.Pin(pyb.Pin.board.PB6, pyb.Pin.OUT_PP)
signal_ch = servo_signal.channel(1, pyb.Timer.PWM, pin=servo_pin, pulse_width=8000)
    
    
    
def fire():
    print('8000')
    signal_ch.pulse_width(8000)
    pyb.delay(350)
    print('16000')
    signal_ch.pulse_width(19000)
    pyb.delay(350)
    
if __name__ == '__main__':
    while True:
        fire()
    #signal_ch.pulse_width(19000)
        

