import pyb

class FireLED:
    def __init__(self, ledPin, timer_num, timerCh1):
        self.ledPin = pyb.Pin(ledPin, pyb.Pin.OUT_PP)
        self.timer = pyb.Timer(timer_num, freq=10)
        self.ch1 = self.timer.channel(timerCh1, pyb.Timer.PWM, pin=self.ledPin, pulse_width_percent = 0)
    
    def on(self):
        self.ch1.pulse_width_percent(100)
        
    def off(self):
        self.ch1.pulse_width_percent(0)
        
    def level(self, level):
        self.ch1.pulse_width_percent(level)
        
    def frequency(self, level):
        self.timer.freq(level)
        
if __name__ == "__main__":
    ledPin = pyb.Pin.board.PB4
    timer = 3
    channel = 1
    LED = FireLED(ledPin, timer, channel)
    while 0:
        LED.level(int(input("Level: ")))
    while 1:
        LED.on()
        LED.level(100)
        for i in range(100):
            LED.frequency(i+1)
            pyb.delay(i*100)
