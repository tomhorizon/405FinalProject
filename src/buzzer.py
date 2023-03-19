import pyb

class Buzzer:
    """! @brief The Buzzer class creates and carries out the functions of a buzzer with the main functionality of beeping at
    different frequencies. Pulse width modification to control the beep frequency
    """
    def __init__(self, buzzerPin, timer_num, timerCh1):
        """! The initialization sets the attributes for a buzzer object
        @param buzzerPin: PYB pin that the buzzer is connected to
        @param timer_num: Timer number used to control the buzzer
        @param timerCh1: Timer channel used to control the buzzer
        """
        self.buzzerPin = pyb.Pin(buzzerPin, pyb.Pin.OUT_PP, pyb.Pin.PULL_DOWN, alt = 1)
        self.timer = pyb.Timer(timer_num, freq=10)
        self.ch1 = self.timer.channel(timerCh1, pyb.Timer.PWM, pin=self.buzzerPin, pulse_width_percent = 0)
    
    def beep(self, psi):
        """! The beep(psi) method causes the buzzer to coninuously beep at a specified frequency (0 --> 100)
        @param psi: Used to control the beep frequency of the buzzer. 
        """
        psi = abs(psi)
        if psi > 100:
            psi = 100
        psi = 100-psi
        if psi < 99:
            self.ch1.pulse_width_percent(psi)
            
    def numBeep(self, n):
        """! The numBeep(n) method causes the buzzer to beep a specified number of times at a fixed frequency
        @param n: Number of beeps
        """
        self.ch1.pulse_width_percent(50)
        pyb.delay(125*n)
        self.ch1.pulse_width_percent(0)
            
    def powerUp(self):
        """! The powerUp() method is used during the wakeUp() method of a turret object and is used to confirm proper
        buzzer function
        """
        self.ch1.pulse_width_percent(50)
        pyb.delay(200)
        self.ch1.pulse_width_percent(0)
        
    def off(self):
        """! The off() method silences the buzzer
        """
        self.ch1.pulse_width_percent(0)
        
        
        
if __name__ == "__main__":
#     Test code used to confirm proper control and function of the buzzer
    buzzerPin = pyb.Pin.board.PA9
    buzzerTimer = 1
    buzzerChannel = 2
    alarm = Buzzer(buzzerPin, buzzerTimer, buzzerChannel)
    while 1:
        alarm.powerUp()
        alarm.beep(int(input("Level: ")))
    while 0:
        for i in range(100):
            alarm.beep(100-i)
            i = i+1
            pyb.delay(i)
    