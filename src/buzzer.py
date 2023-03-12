import pyb

class Buzzer:
    def __init__(self, buzzerPin, timer_num, timerCh1):
        self.buzzerPin = pyb.Pin(buzzerPin, pyb.Pin.OUT_PP, pyb.Pin.PULL_DOWN, alt = 1)
        self.timer = pyb.Timer(timer_num, freq=10)
        self.ch1 = self.timer.channel(timerCh1, pyb.Timer.PWM, pin=self.buzzerPin, pulse_width_percent = 0)
    
    def beep(self, psi):
        psi = abs(psi)
        if psi > 100:
            psi = 100
        psi = 100-psi
        if psi < 99:
            self.ch1.pulse_width_percent(psi)
            
    def powerUp(self):
        self.ch1.pulse_width_percent(50)
        pyb.delay(250)
        self.ch1.pulse_width_percent(0)
        
    def off(self):
        self.ch1.pulse_width_percent(0)
        
        
        
if __name__ == "__main__":
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
    