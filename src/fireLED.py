import pyb

class FireLED:
    """! @brief FireLED controls the brightness and blink frequency of an LED
    """
    def __init__(self, ledPin, timer_num, timerCh1):
        """! The initialization specifies the pin, timer, and channel numbers of an LED object
        @param ledPin: PYB pin that the LED is connected to
        @param tim_num: Timer number used to control the LED
        @param timerCh1: Timer channel number used to control the LED
        """
        self.ledPin = pyb.Pin(ledPin, pyb.Pin.OUT_PP)
        self.timer = pyb.Timer(timer_num, freq=500)
        self.ch1 = self.timer.channel(timerCh1, pyb.Timer.PWM, pin=self.ledPin, pulse_width_percent = 0)
    
    def on(self):
        """! The on() method turns a FireLED object on at 100% brightness
        """
        self.ch1.pulse_width_percent(100)
        
    def off(self):
        """! The on() method turns a FireLED object off
        """
        self.ch1.pulse_width_percent(0)
        
    def level(self, level):
        """! The level(level) method sets the PWM duty cycle of the LED's pin to a specified value to control
        the LED's brightness
        @param level: PWM duty cycle value of LED
        """
        self.ch1.pulse_width_percent(level)
        
    def frequency(self, level):
        """! The frequency(level) method sets the frequency at which the LED blinks
        """
        self.timer.freq(level)
        
    def powerUp(self):
        """! The powerUp() method is used during a turret's wakeUp() method. It causes the LED's to blink, allowing
        the user to visually confirm proper LED control and function
        """
        self.ch1.pulse_width_percent(0)
        self.timer.freq(500)
        for i in range(70):
            self.ch1.pulse_width_percent(i)
            pyb.delay(50)
        self.timer.freq(10)
        self.ch1.pulse_width_percent(100)
        
    def hunt(self):
        """! Dims LED's to 30% duty cycle while the turret is in "hunt" mode
        """
        self.ch1.pulse_width_percent(30)
        
        
if __name__ == "__main__":
    LEDpin = pyb.Pin.board.PA8
    LEDtimer = 1
    LEDchannel = 1
    LED = FireLED(LEDpin, LEDtimer, LEDchannel)
    LED.powerUp()
    while 1:
        LED.level(int(input("Level: ")))
    
