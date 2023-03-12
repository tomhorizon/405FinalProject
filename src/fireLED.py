import pyb

class FireLED:
    def __init__(self, ledPin, timer_num, timerCh1):
        self.ledPin = pyb.Pin(ledPin, pyb.Pin.OUT_PP)
        self.timer = pyb.Timer(timer_num, freq=500)
        self.ch1 = self.timer.channel(timerCh1, pyb.Timer.PWM, pin=self.ledPin, pulse_width_percent = 0)
    
    def on(self):
        self.ch1.pulse_width_percent(100)
        
    def off(self):
        self.ch1.pulse_width_percent(0)
        
    def level(self, level):
        self.ch1.pulse_width_percent(level)
        
    def frequency(self, level):
        self.timer.freq(level)
        
    def powerUp(self):
        self.ch1.pulse_width_percent(0)
        self.timer.freq(500)
        for i in range(70):
            self.ch1.pulse_width_percent(i)
            pyb.delay(50)
        self.timer.freq(10)
        self.ch1.pulse_width_percent(100)
        
    def hunt(self):
        self.ch1.pulse_width_percent(30)
        
        
if __name__ == "__main__":
    LEDpin = pyb.Pin.board.PA8
    LEDtimer = 1
    LEDchannel = 1
    LED = FireLED(LEDpin, LEDtimer, LEDchannel)
    LED.powerUp()
    while 1:
        LED.level(int(input("Level: ")))
    
